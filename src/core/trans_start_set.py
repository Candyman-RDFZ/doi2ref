"""Called when the user clicks on the 'Next' button on the start page.
Initializes validity check and calls the fetcher. When all is well, sets
the main state to 'set'.
"""

from PySide6.QtCore import QEventLoop
from PySide6.QtWidgets import QMessageBox
from .checker import chk_all
from .fetcher import DOIFetcher

def fetch_dois(doi_list: list):
	results = {}
	errors = {}
	cancelled = False
	client = DOIFetcher()
"""
    def fetch_batch(doi_list: list):
		nonlocal client
		loop = QEventLoop()
"""
def trans_start_set(parent, data, dialog_min_size):
	if data is None:
		dialog = QMessageBox.critical(parent, 'Error - doi2ref', 'The DOI table cannot be empty.', buttons=QMessageBox.Ok)
		return None

	parent.content_widget.setEnabled(False)

	# Starts validity check
	parent.start_next_button.setText('Checking...')
	res = chk_all(parent, data)
	if res == 'canceled':
		# Restore the widgets
		parent.content_widget.setEnabled(True)
		parent.start_next_button.setText('Next >')
		return None
	parent.doi_table_widget.set_value(data, True)

	# Extract the DOI numbers
	count = data['count']
	doi_nums = []
	for i in range(count):
		cur_dict = data[str(i + 1)]
		doi_nums.append(cur_dict['doi_num'])
	print(doi_nums)
	fetch_dois(doi_nums)
