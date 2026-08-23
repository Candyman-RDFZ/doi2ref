"""Handles the draft import/exporting."""

from PySide6.QtCore import QSettings, QStandardPaths
from PySide6.QtWidgets import QFileDialog, QMessageBox
import json

def import_draft_file(parent, doi_table):
	settings = QSettings()

	# We use the same 'last_dir' as the export function to open where the user previously saved files 
	last_dir = settings.value('last_dir', QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))
	filename, _ = QFileDialog.getOpenFileName(parent, 'Import Draft - doi2ref', last_dir, 'JSON Files (*.json)')
	
	# User clicked cancel 
	if not filename:
		return None
	
	try:
		with open(filename, 'r') as file:
			data = json.load(file)
	except Exception:
		# json cannot load the file. This indicates that the user did not choose a valid file.
		dialog = QMessageBox.critical(parent, 'Error - doi2ref', f'Error when loading file "{filename}". The file is probably corrupted.', buttons=QMessageBox.Ok)
		return None
	
	# For some reason the user selected an empty json file 
	if data is None:
		return None
	doi_table.set_value(data)

def export_draft_file(parent, data):
	settings = QSettings()
	last_dir = settings.value('last_dir', QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))
	filename, _ = QFileDialog.getSaveFileName(parent, 'Export Draft - doi2ref', last_dir + '/Untitled_Draft.json', 'JSON Files (*.json)')

	# We add a '.json' extension automatically if the user did not enter one.
	if not filename.lower().endswith('.json'):
		filename += '.json'
	with open(filename, 'w') as file:
		# Uses indent=4 to pretty-print such that advanced users will be able to debug
		json.dump(data, file, indent=4)
