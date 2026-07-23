from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListView,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from gui.widgets.plotting.plot_canvas import PlotCanvas


class ProfessionalComboBox(QComboBox):
    """Non-native, wide combo popup with clear highlighted selection."""

    def __init__(self) -> None:
        super().__init__()
        view = QListView()
        view.setObjectName("comboPopup")
        view.setMinimumWidth(285)
        view.setSpacing(2)
        view.setUniformItemSizes(True)
        self.setView(view)
        self.setMinimumWidth(220)
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)

    def showPopup(self) -> None:
        self.view().setCurrentIndex(self.model().index(self.currentIndex(), 0))
        super().showPopup()


class AspectRatioContainer(QWidget):
    """Keeps the graph canvas at a 3:4 width-to-height ratio."""

    def __init__(self, child: QWidget) -> None:
        super().__init__()
        self.child = child
        self.child.setParent(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, event) -> None:
        available_width = self.width()
        available_height = self.height()
        target_width = min(available_width, int(available_height * 3 / 4))
        target_height = int(target_width * 4 / 3)

        if target_height > available_height:
            target_height = available_height
            target_width = int(target_height * 3 / 4)

        x = (available_width - target_width) // 2
        y = (available_height - target_height) // 2
        self.child.setGeometry(x, y, target_width, target_height)
        super().resizeEvent(event)


class GraphWidget(QWidget):
    """Displays PK plots and graph controls."""

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
        controls.setContentsMargins(5, 3, 5, 3)

        controls.addWidget(QLabel("Graph Type"))
        self.scale_selector = ProfessionalComboBox()
        self.scale_selector.addItem("Semi-logarithmic Y-axis", "log")
        self.scale_selector.addItem("Linear Y-axis", "linear")
        self.scale_selector.currentIndexChanged.connect(self._on_scale_changed)
        controls.addWidget(self.scale_selector)
        controls.addStretch()

        self.canvas = PlotCanvas()
        self.aspect_container = AspectRatioContainer(self.canvas)
        layout.addLayout(controls)
        layout.addWidget(self.aspect_container, 1)

    def plot_profile(
        self,
        time: list[float],
        concentration: list[float],
        fitted_time: list[float] | None = None,
        fitted_concentration: list[float] | None = None,
        highlighted_time: list[float] | None = None,
        highlighted_concentration: list[float] | None = None,
    ) -> None:
        self._last_plot_data = {
            "time": time,
            "concentration": concentration,
            "fitted_time": fitted_time,
            "fitted_concentration": fitted_concentration,
            "highlighted_time": highlighted_time,
            "highlighted_concentration": highlighted_concentration,
        }
        self._redraw()

    def clear_plot(self) -> None:
        self._last_plot_data = {
            "time": [],
            "concentration": [],
            "fitted_time": None,
            "fitted_concentration": None,
            "highlighted_time": None,
            "highlighted_concentration": None,
        }
        self.canvas.clear_plot()

    def _on_scale_changed(self) -> None:
        self.canvas.set_scale_mode(str(self.scale_selector.currentData()))
        self._redraw()

    def _redraw(self) -> None:
        self.canvas.plot_profile(**self._last_plot_data)
