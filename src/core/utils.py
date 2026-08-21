"""Misc utility functions for doi2ref

The contents of this file is licensed under the MIT License. See the LICENSE
file for details.

Defines misc utility functions used in the program.
"""

from PySide6.QtCore import QSize
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget

# Window property query function
def get_window_dimension() -> QSize:
	screen = QGuiApplication.primaryScreen()
	width = screen.size().width() // 2
	height = width * 4 // 5
	return QSize(width, height)

# Fontsize query functions
def get_title_fontsize(window_size: QSize) -> int:
	return window_size.height() // 30

def get_text_fontsize(window_size: QSize) -> int:
	return window_size.height() // 50

# Change the widget font to text_fontsize
def change_widget_fontsize(widget: QWidget, size: int) -> None:
	font = widget.font()
	font.setPointSize(size)
	widget.setFont(font)
	return None
