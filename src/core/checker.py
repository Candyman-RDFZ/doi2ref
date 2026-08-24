"""Performs validity check when the user clicks Next in the start page.
This file is necessary to ensure that the data passed to the fetcher is 
correct and contains no empty, conflicting, or duplicate references.
"""

from PySide6.QtWidgets import QMessageBox, QDialog
from ui.checker_dialog import RefEmptyDialog, RefConfdupDialog

def remove_ref(data, idx):
	count = data['count']
	for i in range(idx, count):
		data[str(i)] = data[str(i + 1)]
	del data[str(count)]
	data['count'] -= 1

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

def chk_all(parent, data):
	# Check for empty references
	ref_idx = 0
	while ref_idx < data['count']:
		while True:
			cur_dict = data[str(ref_idx + 1)]
			res = chk_empty(cur_dict)
			if res is None:
				ref_idx += 1
				break

			if isinstance(res, tuple): # All are empty
				dialog = RefEmptyDialog(parent, ref_idx + 1, False, False, None, None)
				if dialog.exec() != QDialog.Accepted:
					return 'canceled'
				nxt_val = dialog.values()
				if nxt_val is None:
					remove_ref(data, ref_idx + 1)
					break
				data[str(ref_idx + 1)]['ref_name'] = nxt_val[0]
				data[str(ref_idx + 1)]['doi_num'] = nxt_val[1]
			elif res == 'ref_name':
				dialog = RefEmptyDialog(parent, ref_idx + 1, False, True, None, cur_dict['doi_num'])
				if dialog.exec() != QDialog.Accepted:
					return 'canceled'
				nxt_val = dialog.values()
				if nxt_val is None:
					remove_ref(data, ref_idx + 1)
					break
				data[str(ref_idx + 1)]['ref_name'] = nxt_val
			elif res == 'doi_num':
				dialog = RefEmptyDialog(parent, ref_idx + 1, True, False, cur_dict['ref_name'], None)
				if dialog.exec() != QDialog.Accepted:
					return 'canceled'
				nxt_val = dialog.values()
				if nxt_val is None:
					remove_ref(data, ref_idx + 1)
					break
				data[str(ref_idx + 1)]['doi_num'] = nxt_val
		
		if ref_idx < data['count']:
			ref_idx += 1
	
	# Check for conflicting or duplicating references
	ref_idx1 = 0
	while ref_idx1 < data['count']:
		ref_idx2 = ref_idx1 + 1
		while ref_idx2 < data['count']:
			while True:
				if ref_idx2 >= data['count']: break
				idx1_data = data[str(ref_idx1 + 1)]
				idx2_data = data[str(ref_idx2 + 1)]
				res = chk_conf_dup(idx1_data, idx2_data)
				if res is None:
					ref_idx2 += 1
					break
				dialog = RefConfdupDialog(parent, res, ref_idx1 + 1, ref_idx2 + 1, idx1_data, idx2_data)
				if dialog.exec() != QDialog.Accepted:
					return 'canceled'
				nxt_val = dialog.values()
				if not nxt_val['has_1'] and not nxt_val['has_2']:
					remove_ref(data, ref_idx1 + 1)
					remove_ref(data, ref_idx2)
					break
				if not nxt_val['has_1']:
					remove_ref(data, ref_idx1 + 1)
					ref_idx2 = ref_idx1 + 1
					break
				if not nxt_val['has_2']:
					remove_ref(data, ref_idx2 + 1)
					continue
				data[str(ref_idx1 + 1)] = nxt_val['1']
				data[str(ref_idx2 + 1)] = nxt_val['2']
		if ref_idx1 < data['count']:
			ref_idx1 += 1
	return data
