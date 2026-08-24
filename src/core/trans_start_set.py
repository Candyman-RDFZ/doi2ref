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

	parent.start_next_button.setEnabled(False)

	# Starts validity check
	parent.start_next_button.setText('Checking...')
	res = chk_all(parent, data)
	if res == 'canceled':
		# Restore the button
		parent.start_next_button.setEnabled(True)
		parent.start_next_button.setText('Next >')
		return None
	parent.doi_table_widget.set_value(data, True)
