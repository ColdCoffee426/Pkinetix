from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem
)


class DataTableWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.table = QTableWidget(0, 2) 
        self.table.setHorizontalHeaderLabels([
            "Time",
            "Concentration"
        ])

        layout.addWidget(self.table)

        self.setLayout(layout)