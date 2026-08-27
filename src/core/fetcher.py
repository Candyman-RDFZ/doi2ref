"""Fetches the DOI metadata from https://doi.org/<DOI>.
Supports batch fetching and async requests.
"""

from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import json
import re

class DOIFetcher(QObject):
	metadata_received = Signal(int, str, dict) # index, DOI, metadata
	error_signal = Signal(int, str, str, str) # index, DOI, errtype, msg
	progress_signal = Signal(int, int) # done, total
	finished_signal = Signal()

	def __init__(self, parent):
		super().__init__(parent)
		self.manager = QNetworkAccessManager(self)
		self.max_connections = 6
		self.queue = []
		self.active = 0
		self.total = 0
		self.done = 0
	
	def fetch_batch(self, dois: list):
		self.queue = [(i, clean_doi(doi)) for i, doi in enumerate(dois)]
		self.total = len(self.queue)
		if self.total == 0:
			self.finished.emit()
			return None
		self._start_next()
	
	def _start_next(self):
		while self.queue and self.active < self.max_connections:
			index, doi = self.queue.pop(0)
			if not valid_doi(doi):
				self._fail(index, doi, 'invalid', 'Invalid DOI format')
				continue
			self.active += 1
			self._fetch_doi(index, doi)
		self._chk_finished()
	
	def _fetch_doi(self, index, doi):
		request = QNetworkRequest(QUrl('https://doi.org/' + doi))
		request.setRawHeader(b'User-Agent', b'doi2ref/0.0.0-pre (mailto:dckx18@gmail.com)')
		request.setRawHeader(b'Accept', b'application/vnd.citationstyles.csl+json')
		reply = self.manager.get(request)
		reply.index = index
		reply.doi = doi
		reply.finished.connect(lambda: self._handle_doi(reply))
	
	def _handle_doi(self, reply):
		index = reply.index
		doi = reply.doi
		status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
		network_err = reply.error()
		err_str = reply.errorString()
		data = bytes(reply.readAll())
		reply.deleteLater()

		if network_err == QNetworkReply.NoError:
			try:
				metadata = json.loads(data)
				self._success(index, doi, metadata)
				return None
			except Exception:
				# The DOI exists but the JSON was unusable.
				self._fetch_crossref(index, doi)
				return None

		if status == 404:
			self._fetch_crossref(index, doi)
			return None

		if status is not None:
			self._fail(index, doi, 'network', f'HTTP error {status} ({err_str}) when fetching https://doi.org/{doi}')
			return None

		self._fail(index, doi, 'network', err_str)
	
	def _fetch_crossref(self, index, doi):
		request = QNetworkRequest(QUrl('https://api.crossref.org/works' + doi))
		reply = self.manager.get(request)
		reply.index = index
		reply.doi = doi
		reply.finished.connect(lambda: self._handl_crossref(reply))
	
	def _handle_crossref(self, reply):
		index = reply.index
		doi = reply.doi
		status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
		network_err = reply.error()
		err_str = reply.errorString()
		data = bytes(reply.readAll())
		reply.deleteLater()

		if network_err == QNetworkReply.NoError:
			try:
				response = json.loads(data)
				metadata = response['message']
				self._success(index, doi, metadata)
				return None
			except (json.JSONDecodeError, KeyError, TypeError) as e:
				self._fail(index, doi, 'metadata', f'Invalid metadata: {e}')
				return None
		
		if status == 404:
			self._fail(index, doi, 'not_found', 'DOI not found')
			return None

		if status is not None:
			self._fail(index, doi, 'network', f'HTTP error {status} ({err_str}) when fetching Crossref.')
	
	def _success(self, index, doi, metadata):
		self.metadata_received.emit(index, doi)
		self.active -= 1
		self.done += 1
		self.progress.emit(self.done, self.total)
		self._start_next()
	
	def _fail(self, index, doi, errtype, msg):
		self.error.emit(index, doi, errtype, msg)
		self.done += 1
		self.progress.emit(self.done, self.total)
		if errtype != 'invalid':
			self.active -= 1
		self._start_next()
	
	def _chk_finished(self):
		if not self.queue and self.active == 0:
			self.finished.emit()
