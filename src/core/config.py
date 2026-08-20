"""Config file for doi2ref

The contents of this file is licensed under the MIT License. See the LICENSE
file for details.

Stores the constants used throughout the program.
"""

from PySide6.QtCore import QSize
from PySide6.QtGui import QGuiApplication

# Application properties

NAME = 'doi2ref'
VERSION = 'INDEV'
FULL_NAME = NAME + ' ' + VERSION

# Window property query function

def get_window_dimension() -> QSize:
	screen = QGuiApplication.primaryScreen()
	width = screen.size().width() * 3 // 5
	height = width * 4 // 5
	return QSize(width, height)

# Fontsize query functions

def get_title_fontsize(window_size : QSize):
	return window_size.height() // 30

def get_text_fontsize(window_size : QSize):
	return window_size.height() // 50
