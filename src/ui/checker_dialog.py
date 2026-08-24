from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QCheckBox, QLineEdit, QDialogButtonBox

class RefEmptyDialog(QDialog):
	def __init__(self, parent, ref_idx: int, has_ref_name: bool, has_doi_num: bool, ref_name, doi_num):
		super().__init__(parent)
		self.setWindowTitle('Complete reference information - doi2ref')
		
		layout = QVBoxLayout()

		form = QFormLayout()
		if not has_ref_name and not has_doi_num: # All are empty
			self.err_text = QLabel(f'Both the reference name and the DOI number of reference No. {ref_idx} are empty.')
			self.info_text = QLabel('Enter the name and number or delete it below:')
			self.state = 'all'
		elif not has_ref_name:
			self.err_text = QLabel(f'The reference name of reference No. {ref_idx} (DOI {doi_num}) is empty.')
			self.info_text = QLabel('Enter the reference name or delete it below:')
			self.state = 'name'
		else:
			self.err_text = QLabel(f'The DOI number of reference No. {ref_idx} ({ref_name}) is empty.')
			self.info_text = QLabel('Enter the DOI number or delete it below:')
			self.state = 'num'
		form.addRow(self.err_text)
		form.addRow(self.info_text)
		
		self.ref_name_entry = QLineEdit()
		self.doi_num_entry = QLineEdit()

		self.del_ref_chk = QCheckBox('Delete this reference')
		self.del_ref_chk.checkStateChanged.connect(self.upd_entries)
		form.addRow(self.del_ref_chk)

		if self.state == 'all':
			form.addRow('Name: ', self.ref_name_entry)
			form.addRow('DOI Number: ', self.doi_num_entry)
		elif self.state == 'name':
			form.addRow('Name: ', self.ref_name_entry)
		else:
			form.addRow('DOI Number: ', self.doi_num_entry)
		
		button_box = QDialogButtonBox(QDialogButtonBox.Cancel)
		continue_button = self.button_box.addButton('Continue', QDialogButtonBox.AcceptRole)

		button_box.accepted.connect(self.accept)
		button_box.rejected.connect(self.reject)

		layout.addLayout(form)
		layout.addWidget(button_box)
		self.setLayout(layout)
	
	def upd_entries(self, state):
		checked = self.del_ref_chk.isChecked()
		self.ref_name_entry.setEnabled(not checked)
		self.doi_num_entry.setEnabled(not checked)

	def values(self):
		ref_name = self.ref_name_entry.text()
		doi_num = self.doi_num_entry.text()
		if self.del_ref_chk.isChecked():
			return None
		if self.state == 'all':
			return (ref_name, doi_num)
		elif self.state == 'name':
			return ref_name
		else:
			return doi_num

class RefConfdupDialog(QDialog):
	def __init__(self, parent, problem: str, ref_idx1: int, ref_idx2: int, dat_idx1: dict, dat_idx2: dict):
		super().__init__(parent)

		layout = QVBoxLayout()
		form = QFormLayout()

		if problem == 'dup':
			self.err_text = QLabel(f'References No. {ref_idx1} and No. {ref_idx2} appears to be duplicates.')
			self.info_text = QLabel('Correct the data or delete references below:')
		elif problem == 'conf':
			self.err_text = QLabel(f'References No. {ref_idx1} and No. {ref_idx2} conflict each other.')
			self.info_text = QLabel('Correct the data or delete references below:')

		form.addRow(self.err_text)
		form.addRow(self.info_text)
		
		self.del_ref1_chk = QCheckBox(f'Delete reference No. {ref_idx1}')
		self.del_ref1_chk.checkStateChanged.connect(self.update_ref1)
		self.ref1_name_entry = QLineEdit()
		self.ref1_doi_entry = QLineEdit()
		self.ref1_name_entry.setText(dat_idx1['ref_name'])
		self.ref1_doi_entry.setText(dat_idx1['doi_num'])
		form.addRow(self.del_ref1_chk)
		form.addRow(f'Reference {ref_idx1} Name: ', self.ref1_name_entry)
		form.addRow(f'DOI Number: ', self.ref1_doi_entry)

		self.del_ref2_chk = QCheckBox(f'Delete reference No. {ref_idx2}')
		self.del_ref2_chk.checkStateChanged.connect(self.update_ref2)
		self.ref2_name_entry = QLineEdit()
		self.ref2_doi_entry = QLineEdit()
		self.ref2_name_entry.setText(dat_idx2['ref_name'])
		self.ref2_doi_entry.setText(dat_idx2['doi_num'])
		form.addRow(self.del_ref2_chk)
		form.addRow(f'Reference {ref_idx2} Name: ', self.ref2_name_entry)
		form.addRow(f'DOI Number: ', self.ref2_doi_entry)

		button_box = QDialogButtonBox(QDialogButtonBox.Cancel)
		button_box.addButton('Continue', QDialogButtonBox.AcceptRole)

		button_box.accepted.connect(self.accept)
		button_box.rejected.connect(self.reject)

		layout.addLayout(form)
		layout.addWidget(button_box)

		self.setLayout(layout)
	
	def update_ref1(self):
		checked = self.del_ref1_chk.isChecked()
		self.ref1_name_entry.setEnabled(not checked)
		self.ref1_doi_entry.setEnabled(not checked)

	def update_ref2(self):
		checked = self.del_ref2_chk.isChecked()
		self.ref2_name_entry.setEnabled(not checked)
		self.ref2_doi_entry.setEnabled(not checked)
	
	def values(self) -> dict:
		has_1 = not self.del_ref1_chk.isChecked()
		has_2 = not self.del_ref2_chk.isChecked()
		ref1_name = None
		ref1_doi = None
		ref2_name = None
		ref2_doi = None
		if has_1:
			ref1_name = self.ref1_name_entry.text()
			ref1_doi = self.ref1_doi_entry.text()
		if has_2:
			ref2_name = self.ref2_name_entry.text()
			ref2_doi = self.ref2_doi_entry.text()
		return {'has_1': has_1, 'has_2': has_2, '1': {'ref_name': ref1_name, 'doi_num': ref1_doi}, '2': {'ref_name': ref2_name, 'doi_num': ref2_doi}}
