"""Performs validity check when the user clicks Next in the start page.
This file is necessary to ensure that the data passed to the fetcher is 
correct and contains no empty, conflicting, or duplicate references.
"""

from PySide6.QtWidgets import QMessageBox, QDialog
from ui.checker_dialog import RefEmptyDialog

def chk_empty(ref):
	if not ref['ref_name'] and not ref['doi_num']:
		return ('ref_name', 'doi_num')
	elif not ref['ref_name']:
		return 'ref_name'
	elif not ref['doi_num']:
		return 'doi_num'
	else:
		return None

def chk_conf_dup(ref1, ref2):
	state_num = int(ref1['ref_name'] == ref2['ref_name']) + int(ref1['doi_num'] == ref2['doi_num'])
	if state_num == 2: # Duplicate
		return 'dup'
	elif state_num == 1: # Conflict
		return 'conf'
	else:
		return None

def chk_all(parent, data, fetcher_dialog):
	count = data['count']
	
	# Check for empty references
	for ref_idx in range(count):
		while True:
			cur_dict = data[str(ref_idx + 1)]
			res = chk_empty(cur_dict)
			fetcher_dialog.hide()
			if res is None:
				fetcher_dialog.show()
				break

			if isinstance(res, tuple): # All are empty
				fetcher_dialog.hide()
				dialog = RefEmptyDialog(parent, ref_idx + 1, False, False, None, None)
				if dialog.exec() != QDialog.Accepted:
					return 'canceled'
				nxt_val = dialog.values()
				data[str(ref_idx + 1)]['ref_name'] = nxt_val[0]
				data[str(ref_idx + 1)]['doi_num'] = nxt_val[1]
			elif res == 'ref_name':
				fetcher_dialog.hide()
				dialog = RefEmptyDialog(parent, ref_idx + 1, False, True, None, cur_dict['doi_num'])
				if dialog.exec() != QDialog.Accepted:
					return 'canceled'
				nxt_val = dialog.values()
				data[str(ref_idx + 1)]['ref_name'] = nxt_val
			elif res == 'doi_num':
				fetcher_dialog.hide()
				dialog = RefEmptyDialog(parent, ref_idx + 1, True, False, cur_dict['ref_name'], None)
				if dialog.exec() != QDialog.Accepted:
					return 'canceled'
				nxt_val = dialog.values()
				data[str(ref_idx + 1)]['doi_num'] = nxt_val

			continue
	
	# Check for conflicting or duplicating references
	for ref_idx1 in range(count):
		for ref_idx2 in range(count):
			if ref_idx1 == ref_idx2: continue
			idx1_data = data[str(ref_idx1 + 1)]
			idx2_data = data[str(ref_idx2 + 1)]
			res = chk_conf_dup(idx1_data, idx2_data)
			if res == 'dup':
				pass
			elif res == 'conf':
				pass
