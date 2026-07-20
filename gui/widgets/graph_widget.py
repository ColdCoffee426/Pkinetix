from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from gui.widgets.plotting.plot_canvas import PlotCanvas


class GraphWidget(QWidget):
    """
    Widget responsible for displaying PK plots.
    """

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        self.canvas = PlotCanvas()

        layout.addWidget(self.canvas)