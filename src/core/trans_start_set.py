"""Called when the user clicks on the 'Next' button on the start page.
Initializes validity check and calls the fetcher. When all is well, sets
the main state to 'set'.
"""

from PySide6.QtWidgets import QMessageBox
from .checker import chk_all

def trans_start_set(parent, data, dialog_min_size):
	if data is None:
		dialog = QMessageBox.critical(parent, 'Error - doi2ref', 'The DOI table cannot be empty.', buttons=QMessageBox.Ok)
		return None

	# Starts validity check
	res = chk_all(parent, data)
	if res == 'canceled':
		return None
	parent.doi_table_widget.set_value(data, True)
