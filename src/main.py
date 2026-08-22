"""Main file for doi2ref.

The contents of this file is licensed under the MIT License. See the LICENSE
file for details.

Handles the front-end UI.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout
import sys

from core.config import FULL_NAME
from core.utils import get_window_dimension, get_title_fontsize, get_text_fontsize, get_footer_fontsize, change_widget_fontsize

from ui.doi_table import DOITableWidget

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
		self.footer_fontsize = get_footer_fontsize(self.size_)
		
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

		self.add_doi_label = QLabel('Put your DOI number(s) below:')
		self.start_layout.addWidget(self.add_doi_label, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.utility_button_widget = QWidget()
		self.utility_button_layout = QHBoxLayout()
		self.utility_button_widget.setLayout(self.utility_button_layout)
		
		# Control buttons
		self.add_doi_button = QPushButton('Add')
		self.add_doi_button.setShortcut('Ctrl+N')
		change_widget_fontsize(self.add_doi_button, self.text_fontsize)
		self.utility_button_layout.addWidget(self.add_doi_button)
		
		self.edit_doi_button = QPushButton('Edit')
		self.edit_doi_button.setShortcut('Ctrl+E')
		change_widget_fontsize(self.add_doi_button, self.text_fontsize)
		self.utility_button_layout.addWidget(self.edit_doi_button)

		self.delete_doi_button = QPushButton('Delete')
		self.delete_doi_button.setShortcut('Del')
		change_widget_fontsize(self.delete_doi_button, self.text_fontsize)
		self.utility_button_layout.addWidget(self.delete_doi_button)
		
		self.utility_button_widget.setMaximumWidth(self.size().width() // 3)
		self.start_layout.addWidget(self.utility_button_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

		# Table that shows the DOI(s)
		self.doi_table_widget = DOITableWidget(self.add_doi_button, self.edit_doi_button, self.delete_doi_button, self.size().width() * 2 // 3, self)
		change_widget_fontsize(self.doi_table_widget, self.text_fontsize)
		self.doi_table_widget.setMinimumWidth(self.size().width() * 3 // 5)
		self.start_layout.addWidget(self.doi_table_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

		# Import/Export functionality

		self.import_export_layout = QHBoxLayout()
		self.import_export_widget = QWidget()
		self.import_export_widget.setLayout(self.import_export_layout)
		self.import_draft = QPushButton('Import Draft')
		self.import_export_layout.addWidget(self.import_draft)
		
		self.export_draft = QPushButton('Export Draft')
		self.import_export_layout.addWidget(self.export_draft)
		self.import_export_widget.setMaximumWidth(self.size().width() // 3)
		self.start_layout.addWidget(self.import_export_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.start_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.content_layout.addWidget(self.start_widget)

		self.main_layout.addLayout(self.content_layout)
		
		# We add stretch here to force the footer to the bottom of the window.
		self.main_layout.addStretch()

		# Footer
		self.footer_sep = QFrame()
		self.footer_sep.setFrameShape(QFrame.HLine)
		self.main_layout.addWidget(self.footer_sep)

		self.copyright_label = QLabel('Copyright (c) 2026 <a href="https://github.com/Candyman-RDFZ">Candy_man</a>.')

		self.misc_label = QLabel('<a href="https://github.com/Candyman-RDFZ/doi2ref">GitHub repository</a>.')
		change_widget_fontsize(self.copyright_label, self.footer_fontsize)
		change_widget_fontsize(self.misc_label, self.footer_fontsize)
		self.copyright_label.setOpenExternalLinks(True)
		self.misc_label.setOpenExternalLinks(True)
		self.main_layout.addWidget(self.copyright_label, alignment=Qt.AlignmentFlag.AlignHCenter)
		self.main_layout.addWidget(self.misc_label, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_layout.setSpacing(2)
		self.main_widget.setLayout(self.main_layout)
		self.setCentralWidget(self.main_widget)


app = QApplication([])

doi2ref = DOI2ref()
doi2ref.show()

sys.exit(app.exec())
