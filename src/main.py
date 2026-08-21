"""Main file for doi2ref.

The contents of this file is licensed under the MIT License. See the LICENSE
file for details.

Handles the front-end UI.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QWidget, QVBoxLayout, QStackedLayout
import sys

from core.config import FULL_NAME, get_window_dimension, get_title_fontsize, get_text_fontsize


class DOI2ref(QMainWindow):
	def __init__(self):
		super().__init__()

		# We store the current state of the app to keep track of which widgets
		# we should display 
		self.state = 'start'

		# Window settings
		self.setWindowTitle(FULL_NAME)
		self.size_ = get_window_dimension()
		self.resize(self.size_)

		# We use these functions to scale fonts with the window size to comply
		# with differently sized monitors.
		self.title_fontsize = get_title_fontsize(self.size_)
		self.text_fontsize = get_text_fontsize(self.size_)
		
		## Start main UI 

		self.main_widget = QWidget()
		self.main_layout = QVBoxLayout()

		# Title label
		self.title = QLabel('doi2ref')
		self.title.setFont(QFont('Monospace', self.title_fontsize))
		self.main_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)

		# Separator
		self.sep = QFrame()
		self.sep.setFrameShape(QFrame.HLine)
		self.main_layout.addWidget(self.sep)

		# Content
		self.content_layout = QStackedLayout()

		# Starting page
		self.start_layout = QVBoxLayout()
		self.start_widget = QWidget()
		self.start_widget.setLayout(self.start_layout)
		self.content_layout.addWidget(self.start_widget)

		self.main_layout.addLayout(self.content_layout)
		
		# We add stretch here to force the footer to the bottom of the window.
		self.main_layout.addStretch()

		# Footer
		self.footer_sep = QFrame()
		self.footer_sep.setFrameShape(QFrame.HLine)
		self.main_layout.addWidget(self.footer_sep)

		self.footer_label = QLabel('doi2ref by <a href="https://github.com/Candyman-RDFZ">Candy_man</a>. <a href="https://github.com/Candyman-RDFZ/doi2ref">GitHub repository</a>.')
		self.footer_label.setOpenExternalLinks(True)
		self.main_layout.addWidget(self.footer_label, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_layout.setSpacing(5)
		self.main_widget.setLayout(self.main_layout)
		self.setCentralWidget(self.main_widget)


app = QApplication([])

doi2ref = DOI2ref()
doi2ref.show()

sys.exit(app.exec())
