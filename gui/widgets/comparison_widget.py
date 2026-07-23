from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ComparisonWidget(QWidget):
    """
    Future compartmental comparison page.

    It intentionally does not invent calculated concentrations before a
    compartmental model has been fitted.
    """

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        heading = QLabel("Observed vs Calculated Concentrations")
        heading.setObjectName("majorHeading")
        heading.setAlignment(Qt.AlignCenter)
        heading.setFixedHeight(36)
        layout.addWidget(heading)

        self.message = QLabel(
            "Calculated concentrations and optimization parameters will "
            "appear here after a compartmental model is fitted."
        )
        self.message.setWordWrap(True)
        self.message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "Time",
            "Observed Conc.",
            "Calculated Conc.",
            "Difference",
            "% Difference",
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table, 1)

        optimization_heading = QLabel("Optimization Parameters")
        optimization_heading.setObjectName("sectionHeading")
        optimization_heading.setAlignment(Qt.AlignCenter)
        optimization_heading.setFixedHeight(36)
        layout.addWidget(optimization_heading)

        self.optimization_status = QLabel(
            "Model selection, parameter estimation and optimization are "
            "reserved for the compartmental-analysis implementation."
        )
        self.optimization_status.setWordWrap(True)
        self.optimization_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.optimization_status)

    def set_observations(self, rows: list[tuple[float, float]]) -> None:
        self.table.setRowCount(len(rows))
        for row_index, (time, concentration) in enumerate(rows):
            self.table.setItem(row_index, 0, QTableWidgetItem(f"{time:g}"))
            self.table.setItem(
                row_index,
                1,
                QTableWidgetItem(f"{concentration:g}"),
            )
            for column in range(2, 5):
                self.table.setItem(row_index, column, QTableWidgetItem("--"))
