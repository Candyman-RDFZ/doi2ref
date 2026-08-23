"""Called when the user clicks on the 'Next' button on the start page.
Initializes validity check and calls the fetcher. When all is well, sets
the main state to 'set'.
"""

from ui.fetcher_dialog import FetcherDialog
from .checker import chk_all

def trans_start_set(parent, data, dialog_min_size):
	fetcher_dialog = FetcherDialog(parent)
	fetcher_dialog.setMinimumWidth(dialog_min_size)
	fetcher_dialog.show()
	# Starts validity check
	fetcher_dialog.label.setText('Performing validity check...')
	res = chk_all(parent, data, fetcher_dialog)
	if res == 'canceled':
		return None
	fetcher_dialog.label.setText('Performing validity check...successful.')

