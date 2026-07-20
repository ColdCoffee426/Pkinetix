from PySide6.QtCore import Qt

from PySide6.QtGui import QAction

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QHeaderView,
    QAbstractItemView,
    QMenu,
)

class DataTableWidget(QWidget):
    """
    Widget responsible for displaying and editing
    concentration-time data.
    """

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

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setAlternatingRowColors(True)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectItems
        )

        self.table.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.AllEditTriggers
        )

        self.table.setSortingEnabled(False)
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

        self.table.insertRow(
            self.row_count()
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