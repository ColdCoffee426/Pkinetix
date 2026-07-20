from PySide6.QtWidgets import (
    QMainWindow,
    QLabel
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PKinetix")
        self.resize(1400, 900)

        label = QLabel("Pharmaco-Kinetix")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)
