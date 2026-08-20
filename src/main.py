"""Main file for doi2ref.

The contents of this file is licensed under the MIT License. See the LICENSE
file for details.

Handles the front-end UI.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
import sys

from core.config import FULL_NAME, get_window_dimension, get_title_fontsize, get_text_fontsize


class DOI2ref(QMainWindow):
	def __init__(self):
		super().__init__()

		# Window settings
		self.setWindowTitle(FULL_NAME)
		self.size_ = get_window_dimension()
		self.resize(self.size_)

		# We use these functions to scale fonts with the window size to comply
		# with different sized monitors.
		self.title_fontsize = get_title_fontsize(self.size_)
		self.text_fontsize = get_text_fontsize(self.size_)
		
		## Start main UI 

		self.main_widget = QWidget()
		self.main_layout = QVBoxLayout()

		# Title label
		self.title = QLabel('doi2ref')
		self.title.setFont(QFont('Monospace', self.title_fontsize))
		self.main_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.main_layout.addStretch()
		self.main_widget.setLayout(self.main_layout)
		self.setCentralWidget(self.main_widget)


app = QApplication([])

doi2ref = DOI2ref()
doi2ref.show()

sys.exit(app.exec())
