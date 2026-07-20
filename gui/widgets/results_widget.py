from PySide6.QtWidgets import QWidget, QFormLayout, QLabel


class ResultsWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QFormLayout()

        parameters = [
            "Cmax",
            "Tmax",
            "λz",
            "Half-life",
            "AUC0-t",
            "AUC0-inf",
            "AUMC",
            "MRT",
            "Clearance",
            "Vz"
        ]

        self.labels = {}

        for p in parameters:
            label = QLabel("--")
            self.labels[p] = label
            layout.addRow(p, label)

        self.setLayout(layout)