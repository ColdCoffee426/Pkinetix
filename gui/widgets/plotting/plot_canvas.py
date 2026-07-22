from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class PlotCanvas(FigureCanvasQTAgg):
    """
    Reusable Matplotlib canvas for PKinetix.
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
        self.axes.set_title(
            "Concentration-Time Profile"
        )
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Concentration")
        self.axes.grid(True)

    def clear_plot(self) -> None:
        self.axes.clear()
        self._configure_axes()
        self.draw()

    def plot_profile(
        self,
        time: list[float],
        concentration: list[float],
        fitted_time: list[float] | None = None,
        fitted_concentration: list[float] | None = None,
        highlighted_time: list[float] | None = None,
        highlighted_concentration: list[float] | None = None,
    ) -> None:

        self.axes.clear()

        self._configure_axes()

        self.axes.plot(
            time,
            concentration,
            marker="o",
            linewidth=2,
            label="Observed",
        )

        if (
            highlighted_time
            and highlighted_concentration
        ):
            self.axes.scatter(
                highlighted_time,
                highlighted_concentration,
                s=60,
                label="Terminal Phase",
            )

        if (
            fitted_time
            and fitted_concentration
        ):
            self.axes.plot(
                fitted_time,
                fitted_concentration,
                linewidth=2,
                linestyle="--",
                label="λz Fit",
            )

        self.axes.legend()

        self.draw()