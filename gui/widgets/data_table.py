from PySide6.QtCore import (
    QEvent,
    QPoint,
    QSignalBlocker,
    Qt,
    Signal,
)
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHeaderView,
    QLineEdit,
    QMenu,
    QStyledItemDelegate,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.models.observation import ObservationInput


class TableEditorDelegate(QStyledItemDelegate):
    """
    Creates a full-height inline editor for numeric table entries.
    """

    def createEditor(self, parent, option, index) -> QLineEdit:
        editor = QLineEdit(parent)
        editor.setMinimumHeight(30)
        editor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        editor.setContentsMargins(3, 0, 3, 0)
        return editor


class SingleClickEditTable(QTableWidget):
    """
    Starts editing after one stationary click while preserving drag selection.
    """

    def __init__(self, rows: int, columns: int) -> None:
        super().__init__(rows, columns)
        self._press_position = QPoint()
        self._pressed_index = None

    def mousePressEvent(self, event) -> None:
        self._press_position = event.position().toPoint()
        self._pressed_index = self.indexAt(self._press_position)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        release_position = event.position().toPoint()
        distance = (release_position - self._press_position).manhattanLength()
        super().mouseReleaseEvent(event)

        if (
            event.button() == Qt.LeftButton
            and distance <= QApplication.startDragDistance()
            and self._pressed_index is not None
            and self._pressed_index.isValid()
            and not event.modifiers()
        ):
            item = self.item(
                self._pressed_index.row(),
                self._pressed_index.column(),
            )
            if item is not None:
                self.setCurrentItem(item)
                self.editItem(item)


class DataTableWidget(QWidget):
    """
    Editable concentration-time data table.
    """

    data_changed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.time_unit = "h"
        self.concentration_unit = "ng/mL"
        self.table = SingleClickEditTable(0, 2)
        self.table.setItemDelegate(TableEditorDelegate(self.table))
        self._configure_table()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.table)

        for _ in range(12):
            self.add_empty_row()

    def _configure_table(self) -> None:
        self._update_headers()
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.EditKeyPressed
            | QAbstractItemView.SelectedClicked
        )
        self.table.setShowGrid(True)
        self.table.setAlternatingRowColors(False)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(34)
        self.table.verticalHeader().setMinimumSectionSize(34)
        self.table.horizontalHeader().setMinimumHeight(34)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.itemChanged.connect(self._on_item_changed)
        self.table.installEventFilter(self)

    def _update_headers(self) -> None:
        self.table.setHorizontalHeaderLabels([
            f"Time ({self.time_unit})",
            f"Concentration ({self.concentration_unit})",
        ])

    def add_empty_row(self) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.setRowHeight(row, 34)

    def clear_data(self) -> None:
        blocker = QSignalBlocker(self.table)
        self.table.setRowCount(0)
        for _ in range(12):
            self.add_empty_row()
        del blocker
        self.data_changed.emit()

    def set_data(self, rows: list[tuple[float, float]]) -> None:
        blocker = QSignalBlocker(self.table)
        self.table.setRowCount(0)

        for time, concentration in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(f"{time:g}"))
            self.table.setItem(row, 1, QTableWidgetItem(f"{concentration:g}"))
            self.table.setRowHeight(row, 34)

        for _ in range(max(3, 12 - len(rows))):
            self.add_empty_row()

        del blocker
        self.data_changed.emit()

    def get_data(self) -> list[ObservationInput]:
        data: list[ObservationInput] = []

        for row in range(self.table.rowCount()):
            time_item = self.table.item(row, 0)
            concentration_item = self.table.item(row, 1)
            time = time_item.text().strip() if time_item else ""
            concentration = (
                concentration_item.text().strip()
                if concentration_item
                else ""
            )

            if time == "" and concentration == "":
                continue

            data.append(
                ObservationInput(
                    row=row,
                    time=time,
                    concentration=concentration,
                )
            )

        return data

    def convert_time_unit(self, old_unit: str, new_unit: str) -> None:
        if old_unit == new_unit:
            return

        factor = 60.0 if old_unit == "h" and new_unit == "min" else 1 / 60
        self._convert_column(0, factor)
        self.time_unit = new_unit
        self._update_headers()
        self.data_changed.emit()

    def convert_concentration_unit(
        self,
        old_unit: str,
        new_unit: str,
    ) -> None:
        if old_unit == new_unit:
            return

        factor = 1 / 1000 if old_unit == "ng/mL" else 1000.0
        self._convert_column(1, factor)
        self.concentration_unit = new_unit
        self._update_headers()
        self.data_changed.emit()

    def _convert_column(self, column: int, factor: float) -> None:
        blocker = QSignalBlocker(self.table)

        for row in range(self.table.rowCount()):
            item = self.table.item(row, column)
            if item is None or item.text().strip() == "":
                continue

            try:
                value = float(item.text())
            except ValueError:
                continue

            item.setText(f"{value * factor:.10g}")

        del blocker

    def _on_item_changed(self) -> None:
        if self.table.currentRow() == self.table.rowCount() - 1:
            self.add_empty_row()
        self.data_changed.emit()

    def _show_context_menu(self, position) -> None:
        menu = QMenu(self)
        actions = [
            ("Insert Row", self.insert_row),
            ("Delete Selected Rows", self.delete_selected_rows),
            None,
            ("Copy", self.copy_selection),
            ("Cut", self.cut_selection),
            ("Paste", self.paste_selection),
            ("Clear Selected Cells", self.clear_selected_cells),
        ]

        for action_data in actions:
            if action_data is None:
                menu.addSeparator()
                continue

            text, callback = action_data
            action = QAction(text, self)
            action.triggered.connect(callback)
            menu.addAction(action)

        menu.exec(self.table.viewport().mapToGlobal(position))

    def insert_row(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            row = self.table.rowCount()

        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.setRowHeight(row, 34)

    def delete_selected_rows(self) -> None:
        rows = sorted(
            {index.row() for index in self.table.selectedIndexes()},
            reverse=True,
        )

        for row in rows:
            self.table.removeRow(row)

        if self.table.rowCount() == 0:
            self.add_empty_row()

        self.data_changed.emit()

    def clear_selected_cells(self) -> None:
        blocker = QSignalBlocker(self.table)
        for item in self.table.selectedItems():
            item.setText("")
        del blocker
        self.data_changed.emit()

    def copy_selection(self) -> None:
        ranges = self.table.selectedRanges()
        if not ranges:
            return

        selected_range = ranges[0]
        rows = []

        for row in range(selected_range.topRow(), selected_range.bottomRow() + 1):
            values = []
            for column in range(
                selected_range.leftColumn(),
                selected_range.rightColumn() + 1,
            ):
                item = self.table.item(row, column)
                values.append(item.text() if item else "")
            rows.append("\t".join(values))

        QApplication.clipboard().setText("\n".join(rows))

    def cut_selection(self) -> None:
        self.copy_selection()
        self.clear_selected_cells()

    def paste_selection(self) -> None:
        text = QApplication.clipboard().text()
        if not text:
            return

        start_row = max(self.table.currentRow(), 0)
        start_column = max(self.table.currentColumn(), 0)
        rows = text.splitlines()
        blocker = QSignalBlocker(self.table)

        for row_offset, row_text in enumerate(rows):
            values = row_text.split("\t")
            target_row = start_row + row_offset

            while target_row >= self.table.rowCount():
                self.add_empty_row()

            for column_offset, value in enumerate(values):
                target_column = start_column + column_offset
                if target_column >= self.table.columnCount():
                    continue

                item = self.table.item(target_row, target_column)
                if item is None:
                    item = QTableWidgetItem()
                    self.table.setItem(target_row, target_column, item)
                item.setText(value)

        del blocker
        self.data_changed.emit()

    def eventFilter(self, watched, event) -> bool:
        if watched is self.table and event.type() == QEvent.KeyPress:
            if event.matches(QKeySequence.Copy):
                self.copy_selection()
                return True
            if event.matches(QKeySequence.Cut):
                self.cut_selection()
                return True
            if event.matches(QKeySequence.Paste):
                self.paste_selection()
                return True
            if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
                self.clear_selected_cells()
                return True

        return super().eventFilter(watched, event)
