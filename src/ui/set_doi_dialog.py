from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout

class AddEditDialog(QDialog):
	def __init__(self, min_size, parent=None, edit=False, edit_name='', doi_num=''):
		super().__init__(parent)
		self.setWindowTitle('Add reference')
		self.name_edit = QLineEdit()
		self.doi_edit = QLineEdit()

		if edit:
			self.name_edit.setText(edit_name)
			self.doi_edit.setText(doi_num)
		
		self.form = QFormLayout()
		self.form.addRow('Reference Name: ', self.name_edit)
		self.form.addRow('DOI Number or URL: ', self.doi_edit)
		self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)
		
		self.layout = QVBoxLayout()
		self.layout.addLayout(self.form)
		self.layout.addWidget(self.buttons)
		self.setLayout(self.layout)
		self.setMinimumWidth(min_size)
	
	def values(self) -> tuple:
		return (self.name_edit.text(), self.doi_edit.text())
