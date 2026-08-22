from PySide6.QtCore import QSettings, QStandardPaths
from PySide6.QtWidgets import QFileDialog
import json

def import_draft_file(parent, doi_table):
	settings = QSettings()
	last_dir = settings.value('last_dir', QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))
	filename, _ = QFileDialog.getOpenFileName(parent, 'Import Draft - doi2ref', last_dir, 'JSON Files (*.json)')
	with open(filename, 'r') as file:
		data = json.load(file)
	doi_table.set_value(data)

def export_draft_file(parent, data):
	settings = QSettings()
	last_dir = settings.value('last_dir', QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))
	filename, _ = QFileDialog.getSaveFileName(parent, 'Export Draft - doi2ref', last_dir + '/Untitled_Draft.json', 'JSON Files (*.json)')

	if not filename.lower().endswith('.json'):
		filename += '.json'
	with open(filename, 'w') as file:
		json.dump(data, file, indent=4)
