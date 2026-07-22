from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from gui.widgets.plotting.plot_canvas import PlotCanvas


class GraphWidget(QWidget):
    """
    Displays PK plots and graph controls.
    """

    def __init__(self) -> None:
        super().__init__()

        self._last_plot_data = {
            "time": [],
            "concentration": [],
            "fitted_time": None,
            "fitted_concentration": None,
            "highlighted_time": None,
            "highlighted_concentration": None,
        }

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        controls = QHBoxLayout()

        scale_label = QLabel("Graph Scale")

        self.scale_selector = QComboBox()
        self.scale_selector.addItem(
            "Semi-log Y",
            "log",
        )
        self.scale_selector.addItem(
            "Linear",
            "linear",
        )
        self.scale_selector.currentIndexChanged.connect(
            self._on_scale_changed
        )

        controls.addWidget(scale_label)
        controls.addWidget(self.scale_selector)
        controls.addStretch()

        self.canvas = PlotCanvas()

        layout.addLayout(controls)
        layout.addWidget(self.canvas, 1)

    def plot_profile(
        self,
        time: list[float],
        concentration: list[float],
        fitted_time: list[float] | None = None,
        fitted_concentration: list[float] | None = None,
        highlighted_time: list[float] | None = None,
        highlighted_concentration: list[float] | None = None,
    ) -> None:
        """
        Store and display concentration-time data.
        """

        self._last_plot_data = {
            "time": time,
            "concentration": concentration,
            "fitted_time": fitted_time,
            "fitted_concentration": fitted_concentration,
            "highlighted_time": highlighted_time,
            "highlighted_concentration": (
                highlighted_concentration
            ),
        }

        self._redraw()

    def _on_scale_changed(self) -> None:
        """
        Change between linear and semi-log scales.
        """

        mode = str(
            self.scale_selector.currentData()
        )

        self.canvas.set_scale_mode(mode)
        self._redraw()

    def _redraw(self) -> None:
        """
        Redraw the latest profile.
        """

        self.canvas.plot_profile(
            time=self._last_plot_data["time"],
            concentration=(
                self._last_plot_data[
                    "concentration"
                ]
            ),
            fitted_time=(
                self._last_plot_data[
                    "fitted_time"
                ]
            ),
            fitted_concentration=(
                self._last_plot_data[
                    "fitted_concentration"
                ]
            ),
            highlighted_time=(
                self._last_plot_data[
                    "highlighted_time"
                ]
            ),
            highlighted_concentration=(
                self._last_plot_data[
                    "highlighted_concentration"
                ]
            ),
        )