from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QAbstractItemView, QDialog, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView

from .set_doi_dialog import AddEditDialog

class DOITableWidget(QTableWidget):
	def __init__(self, add_button: QPushButton, edit_button: QPushButton, del_button: QPushButton, dialog_min_size: int, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.dialog_min_size = dialog_min_size

		self.add_button = add_button
		self.edit_button = edit_button
		self.del_button = del_button

		self.setColumnCount(2)
		self.setHorizontalHeaderLabels(['Reference Name', 'DOI Number'])
		self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.setSelectionMode(QAbstractItemView.SingleSelection)

		self.setDragEnabled(True)
		self.setAcceptDrops(True)
		self.setDropIndicatorShown(True)
		self.setDragDropMode(QAbstractItemView.DragDrop)
		self.setDefaultDropAction(Qt.MoveAction)
		self.dragged_row = -1
		self.row_cnt = 0
		
		self.add_button.clicked.connect(self.add_row)
		self.edit_button.clicked.connect(self.edit_row)
		self.del_button.clicked.connect(self.del_row)
		self.itemSelectionChanged.connect(self.update_del_edit_button)
		self.update_del_edit_button()
	
	def add_row(self):
		dialog = AddEditDialog(self.dialog_min_size, self.parent, False)
		if dialog.exec() != QDialog.Accepted:
			return None
		name, doi = dialog.values()
		
		self.insertRow(self.row_cnt)
		self.setItem(self.row_cnt, 0, QTableWidgetItem(name))
		self.setItem(self.row_cnt, 1, QTableWidgetItem(doi))
		self.row_cnt += 1 
	
	def edit_row(self):
		sel_rows = self.selectionModel().selectedRows()
		if not sel_rows:
			return None
		row = sel_rows[0].row()
		ref_name = self.item(row, 0).text()
		doi_num = self.item(row, 1).text()
		
		dialog = AddEditDialog(self.dialog_min_size, self.parent, True, ref_name, doi_num)
		if dialog.exec() != QDialog.Accepted:
			return None
		name, doi = dialog.values()
		self.setItem(row, 0, QTableWidgetItem(name))
		self.setItem(row, 1, QTableWidgetItem(doi))

	def del_row(self):
		sel_rows = self.selectionModel().selectedRows()
		if not sel_rows:
			return None
		row = sel_rows[0].row()
		self.removeRow(row)
		self.row_cnt -= 1
	
	def update_del_edit_button(self):
		has_sel = bool(self.selectionModel().selectedRows())
		self.edit_button.setEnabled(has_sel)
		self.del_button.setEnabled(has_sel)

	def startDrag(self, supported_actions):
		sel_rows = self.selectionModel().selectedRows()
		if not sel_rows:
			return None
		self.dragged_row = sel_rows[0].row()
		mime_data = QMimeData()
		drag = QDrag(self)
		drag.setMimeData(mime_data)
		drag.exec(Qt.MoveAction)
		self.dragged_row = -1
	
	def dragEnterEvent(self, event):
		if event.source() is self:
			event.acceptProposedAction()
		else:
			event.ignore()
	
	def dragMoveEvent(self, event):
		if event.source() is self:
			event.acceptProposedAction()
		else:
			event.ignore()
	
	def dropEvent(self, event):
		if event.source() is not self:
			event.ignore()
			return None
		if self.dragged_row < 0:
			event.ignore()
			return None
		pos = event.position().toPoint()
		target = self.rowAt(pos.y())
		if target < 0:
			event.ignore()
			return None
		if target == self.dragged_row:
			event.acceptProposedAction()
			return
		self.swap_rows(self.dragged_row, target)
		self.selectRow(target)
		event.acceptProposedAction()
	
	def swap_rows(self, row1, row2):
		for col in range(2):
			item1 = self.item(row1, col)
			item2 = self.item(row2, col)
			item1 = item1.clone() if item1 else None
			item2 = item2.clone() if item2 else None
			self.setItem(row1, col, item2)
			self.setItem(row2, col, item1)

	def get_value(self):
		if self.row_cnt == 0:
			return None
		res = {}
		res['has_data'] = False
		for row in range(self.row_cnt):
			ref_name = self.item(row, 0).text()
			doi_num = self.item(row, 1).text()
			res[str(row + 1)] = {'ref_name': ref_name, 'doi_num': doi_num}
		return res
