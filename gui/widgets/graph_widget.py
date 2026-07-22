from PySide6.QtWidgets import QWidget, QVBoxLayout
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

    def plot_profile(
        self,
        time: list[float],
        concentration: list[float],
        fitted_time: list[float] | None = None,
        fitted_concentration: list[float] | None = None,
        highlighted_time: list[float] | None = None,
        highlighted_concentration: list[float] | None = None,
    ) -> None:

        self.canvas.plot_profile(
            time,
            concentration,
            fitted_time,
            fitted_concentration,
            highlighted_time,
            highlighted_concentration,
        )