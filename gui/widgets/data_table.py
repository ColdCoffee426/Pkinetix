
from PySide6.QtCore import (
    Qt,
    QEvent,
    Signal,
)
from PySide6.QtGui import QAction, QKeySequence

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QMenu,
    QApplication,
)

class DataTableWidget(QWidget):
    
    """
    Widget responsible for displaying and editing
    concentration-time data.
    """
    data_changed = Signal()


    def __init__(self) -> None:
        super().__init__()

        self._create_table()
        self._create_layout()

        # Temporary empty rows for user entry
        for _ in range(10):
            self.add_empty_row()

    def _create_table(self) -> None:
        """
        Create and configure the data table.
        """

        self.table = QTableWidget(0, 2)

        self.table.setHorizontalHeaderLabels(
            [
                "Time",
                "Concentration",
            ]
        )

        self._configure_table()
        self.table.installEventFilter(self)
        self.table.itemChanged.connect(
            self._on_item_changed
        )

    def _create_layout(self) -> None:
        """
        Create widget layout.
        """

        layout = QVBoxLayout(self)

        layout.addWidget(self.table)

    def _configure_table(self) -> None:
        """
        Configure table behaviour.
        """

        self.table.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectItems
        )

        self.table.setEditTriggers(
            QAbstractItemView.SelectedClicked
            | QAbstractItemView.EditKeyPressed
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setContextMenuPolicy(
            Qt.CustomContextMenu
        )

        self.table.customContextMenuRequested.connect(
            self._show_context_menu
        )

    def row_count(self) -> int:
        """
        Return number of rows.
        """

        return self.table.rowCount()

    def column_count(self) -> int:
        """
        Return number of columns.
        """

        return self.table.columnCount()

    def add_empty_row(self) -> None:
        """
        Add a new empty row.
        """
        
        row = self.row_count()

        self.table.insertRow(row)

        for column in range(self.column_count()):
            self.table.setItem(
                row,
                column,
                QTableWidgetItem("")
            )


    def clear_table(self) -> None:
        """
        Remove all rows.
        """

        self.table.setRowCount(0)
    
    def _show_context_menu(self, position) -> None:
        """
        Display the table context menu.
        """

        menu = QMenu(self)

        insert_action = QAction(
            "Insert Row",
            self
        )

        delete_action = QAction(
            "Delete Selected Rows",
            self
        )

        clear_action = QAction(
            "Clear Selected Cells",
            self
        )

        insert_action.triggered.connect(
            self.add_empty_row
        )

        delete_action.triggered.connect(
            self.delete_selected_rows
        )

        clear_action.triggered.connect(
            self.clear_selected_cells
        )

        menu.addAction(insert_action)
        menu.addAction(delete_action)
        menu.addSeparator()
        menu.addAction(clear_action)

        menu.exec(
            self.table.viewport().mapToGlobal(position)
        )

    def delete_selected_rows(self) -> None:
        """
        Delete selected rows from the table.
        """

        selected_rows = sorted(
            {
                index.row()
                for index in self.table.selectedIndexes()
            },
            reverse=True,
        )

        for row in selected_rows:
            self.table.removeRow(row)

    def clear_selected_cells(self) -> None:
        """
        Clear contents of selected cells.
        """

        for item in self.table.selectedItems():
            item.setText("")

    def copy_selection(self) -> None:
        """
        Copy selected cells to clipboard.
        """

        selected = self.table.selectedRanges()

        if not selected:
            return

        clipboard_text = ""

        selected_range = selected[0]

        for row in range(
            selected_range.topRow(),
            selected_range.bottomRow() + 1
        ):

            row_data = []

            for column in range(
                selected_range.leftColumn(),
                selected_range.rightColumn() + 1
            ):

                item = self.table.item(
                    row,
                    column
                )

                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")

            clipboard_text += "\t".join(row_data)
            clipboard_text += "\n"

        clipboard = QApplication.clipboard()

        clipboard.setText(
            clipboard_text.rstrip("\n")
        )


    def paste_selection(self) -> None:
        """
        Paste tab-separated clipboard data.
        """

        clipboard = QApplication.clipboard()

        text = clipboard.text()

        if not text:
            return

        rows = text.splitlines()

        start_row = self.table.currentRow()
        start_column = self.table.currentColumn()

        for row_index, row_data in enumerate(rows):

            columns = row_data.split("\t")

            for column_index, value in enumerate(columns):

                row = start_row + row_index
                column = start_column + column_index

                if row >= self.table.rowCount():
                    self.table.insertRow(row)

                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value)
                )

    def cut_selection(self) -> None:
        """
        Copy then clear selected cells.
        """

        self.copy_selection()

        self.clear_selected_cells()

    def eventFilter(self, obj, event):
        """
        Handle table keyboard shortcuts.
        """

        if obj == self.table:

            if event.type() == QEvent.Type.KeyPress:

                if event.matches(
                    QKeySequence.StandardKey.Copy
                ):
                    self.copy_selection()
                    return True

                elif event.matches(
                    QKeySequence.StandardKey.Paste
                ):
                    self.paste_selection()
                    return True

                elif event.matches(
                    QKeySequence.StandardKey.Cut
                ):
                    self.cut_selection()
                    return True

        return super().eventFilter(obj, event)
    
    def _on_item_changed(self) -> None:
        """
        Emit signal when table data changes.
        """

        self.data_changed.emit()

    def get_data(self) -> list[tuple[str, str]]:
        """
        Return table contents.

        Returns:
            List of (time, concentration) pairs.
        """

        data = []

        for row in range(self.table.rowCount()):

            time_item = self.table.item(row, 0)
            concentration_item = self.table.item(row, 1)

            time = (
                time_item.text()
                if time_item
                else ""
            )

            concentration = (
                concentration_item.text()
                if concentration_item
                else ""
            )

            data.append(
                (
                    time,
                    concentration,
                )
            )

        return data