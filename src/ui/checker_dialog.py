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
			self.info_text = QLabel('Enter the name and number below:')
			self.state = 'all'
		elif not has_ref_name:
			self.err_text = QLabel(f'The reference name of reference No. {ref_idx} (DOI {doi_num}) is empty.')
			self.info_text = QLabel('Enter the reference name below:')
			self.state = 'name'
		else:
			self.err_text = QLabel(f'The DOI number of reference No. {ref_idx} ({ref_name}) is empty.')
			self.info_text = QLabel('Enter the DOI number below:')
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
		
		self.button_box = QDialogButtonBox(QDialogButtonBox.Cancel)
		continue_button = self.button_box.addButton('Continue', QDialogButtonBox.AcceptRole)

		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)

		layout.addLayout(form)
		layout.addWidget(self.button_box)
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
	def __init__(self, parent, problem, ref_idx1, ref_idx2, dat_idx1, dat_idx2):
		super().__init__(parent)

		layout = QVBoxLayout()
		form = QFormLayout()
		
#		if problem == 
