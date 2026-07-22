from PySide6.QtCore import QEvent, QSignalBlocker, Qt, Signal
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHeaderView,
    QMenu,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.models.observation import ObservationInput


class DataTableWidget(QWidget):
    """
    Editable concentration-time data table.
    """

    data_changed = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.time_unit = "h"
        self.concentration_unit = "ng/mL"

        self.table = QTableWidget(0, 2)
        self._configure_table()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.table)

        for _ in range(12):
            self.add_empty_row()

    def _configure_table(self) -> None:
        self._update_headers()

        self.table.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectItems
        )
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.EditKeyPressed
            | QAbstractItemView.SelectedClicked
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(
            self._show_context_menu
        )
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

    def convert_time_unit(
        self,
        old_unit: str,
        new_unit: str,
    ) -> None:
        if old_unit == new_unit:
            return

        factor = 1.0

        if old_unit == "h" and new_unit == "min":
            factor = 60.0
        elif old_unit == "min" and new_unit == "h":
            factor = 1 / 60

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

        factor = 1.0

        if old_unit == "ng/mL" and new_unit == "µg/mL":
            factor = 1 / 1000
        elif old_unit == "µg/mL" and new_unit == "ng/mL":
            factor = 1000.0

        self._convert_column(1, factor)
        self.concentration_unit = new_unit
        self._update_headers()
        self.data_changed.emit()

    def _convert_column(
        self,
        column: int,
        factor: float,
    ) -> None:
        blocker = QSignalBlocker(self.table)

        for row in range(self.table.rowCount()):
            item = self.table.item(row, column)

            if item is None:
                continue

            text = item.text().strip()

            if text == "":
                continue

            try:
                value = float(text)
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

        insert_action = QAction("Insert Row", self)
        delete_action = QAction("Delete Selected Rows", self)
        copy_action = QAction("Copy", self)
        cut_action = QAction("Cut", self)
        paste_action = QAction("Paste", self)
        clear_action = QAction("Clear Selected Cells", self)

        insert_action.triggered.connect(self.insert_row)
        delete_action.triggered.connect(
            self.delete_selected_rows
        )
        copy_action.triggered.connect(self.copy_selection)
        cut_action.triggered.connect(self.cut_selection)
        paste_action.triggered.connect(self.paste_selection)
        clear_action.triggered.connect(
            self.clear_selected_cells
        )

        menu.addAction(insert_action)
        menu.addAction(delete_action)
        menu.addSeparator()
        menu.addAction(copy_action)
        menu.addAction(cut_action)
        menu.addAction(paste_action)
        menu.addAction(clear_action)

        menu.exec(
            self.table.viewport().mapToGlobal(position)
        )

    def insert_row(self) -> None:
        row = self.table.currentRow()

        if row < 0:
            row = self.table.rowCount()

        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))

    def delete_selected_rows(self) -> None:
        rows = sorted(
            {
                index.row()
                for index in self.table.selectedIndexes()
            },
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

        for row in range(
            selected_range.topRow(),
            selected_range.bottomRow() + 1,
        ):
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

                item = self.table.item(
                    target_row,
                    target_column,
                )

                if item is None:
                    item = QTableWidgetItem()
                    self.table.setItem(
                        target_row,
                        target_column,
                        item,
                    )

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