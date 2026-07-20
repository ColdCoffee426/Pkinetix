from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class GraphWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Graph will appear here")
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)

        self.setLayout(layout)