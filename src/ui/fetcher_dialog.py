from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class FetcherDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.allow_close = False
		self.setWindowTitle('Fetching... - doi2ref')
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)

		layout = QVBoxLayout(self)
		self.label = QLabel('Starting...')
		layout.addWidget(self.label)

		self.abort_button = QPushButton('Abort')
		self.abort_button.clicked.connect(self.abort)
		layout.addWidget(self.abort_button)
		self.setLayout(layout)
	
	def closeEvent(self, event):
		if not self.allow_close:
			event.ignore()
		else:
			event.accept()

	def abort(self):
		self.allow_close = True
		self.close()
