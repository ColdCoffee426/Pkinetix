from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class PlotCanvas(FigureCanvasQTAgg):
    """
    Reusable Matplotlib canvas for PKinetix.

    All plotting functionality is implemented here.
    """

    def __init__(self) -> None:

        self.figure = Figure(
            figsize=(5, 4),
            tight_layout=True,
        )

        super().__init__(self.figure)

        self.axes = self.figure.add_subplot(111)

        self._configure_axes()

    def _configure_axes(self) -> None:
        """
        Configure default appearance.
        """

        self.axes.set_title("Concentration-Time Profile")

        self.axes.set_xlabel("Time")

        self.axes.set_ylabel("Concentration")

        self.axes.grid(True)

    def clear_plot(self) -> None:
        """
        Clear the graph.
        """

        self.axes.clear()

        self._configure_axes()

        self.draw()

    def plot_profile(
        self,
        time: list[float],
        concentration: list[float],
    ) -> None:
        """
        Plot concentration-time profile.
        """

        self.axes.clear()

        self._configure_axes()

        self.axes.plot(
            time,
            concentration,
            marker="o",
            linewidth=2,
        )

        self.draw()