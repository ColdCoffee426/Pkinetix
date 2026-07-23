from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import (
    FuncFormatter,
    LogLocator,
    NullFormatter,
)


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
        self.scale_mode = "log"

        self._configure_axes()

    def _configure_axes(self) -> None:
        """
        Configure the concentration-time graph.
        """

        self.axes.set_title(
            "Concentration-Time Profile"
        )
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Concentration")

        if self.scale_mode == "log":
            self.axes.set_yscale("log")

            self.axes.yaxis.set_major_locator(
                LogLocator(base=10.0)
            )

            self.axes.yaxis.set_minor_locator(
                LogLocator(
                    base=10.0,
                    subs=tuple(range(2, 10)),
                )
            )

            self.axes.yaxis.set_major_formatter(
                FuncFormatter(
                    lambda value, _: f"{value:g}"
                )
            )

            self.axes.yaxis.set_minor_formatter(
                NullFormatter()
            )

            self.axes.grid(
                True,
                which="major",
                linewidth=0.9,
            )

            self.axes.grid(
                True,
                which="minor",
                linewidth=0.35,
                alpha=0.55,
            )
        else:
            self.axes.set_yscale("linear")

            self.axes.grid(
                True,
                which="major",
                linewidth=0.8,
            )

    def set_scale_mode(
        self,
        mode: str,
    ) -> None:
        """
        Set graph scale to linear or semi-log.
        """

        if mode not in ("linear", "log"):
            raise ValueError(
                "Graph scale must be linear or log."
            )

        self.scale_mode = mode

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
        fitted_time: list[float] | None = None,
        fitted_concentration: list[float] | None = None,
        highlighted_time: list[float] | None = None,
        highlighted_concentration: list[float] | None = None,
    ) -> None:
        """
        Plot observed and fitted concentration-time data.
        """

        self.axes.clear()
        self._configure_axes()

        valid_time = []
        valid_concentration = []

        for time_value, concentration_value in zip(
            time,
            concentration,
        ):
            if (
                self.scale_mode == "log"
                and concentration_value <= 0
            ):
                continue

            valid_time.append(time_value)
            valid_concentration.append(
                concentration_value
            )

        if valid_time:
            self.axes.plot(
                valid_time,
                valid_concentration,
                marker="o",
                linewidth=1.8,
                label="Observed",
            )

        if (
            highlighted_time
            and highlighted_concentration
        ):
            valid_highlighted_time = []
            valid_highlighted_concentration = []

            for time_value, concentration_value in zip(
                highlighted_time,
                highlighted_concentration,
            ):
                if (
                    self.scale_mode == "log"
                    and concentration_value <= 0
                ):
                    continue

                valid_highlighted_time.append(
                    time_value
                )
                valid_highlighted_concentration.append(
                    concentration_value
                )

            if valid_highlighted_time:
                self.axes.scatter(
                    valid_highlighted_time,
                    valid_highlighted_concentration,
                    s=65,
                    label="Terminal Phase",
                    zorder=3,
                )

        if fitted_time and fitted_concentration:
            valid_fitted_time = []
            valid_fitted_concentration = []

            for time_value, concentration_value in zip(
                fitted_time,
                fitted_concentration,
            ):
                if (
                    self.scale_mode == "log"
                    and concentration_value <= 0
                ):
                    continue

                valid_fitted_time.append(time_value)
                valid_fitted_concentration.append(
                    concentration_value
                )

            if valid_fitted_time:
                self.axes.plot(
                    valid_fitted_time,
                    valid_fitted_concentration,
                    linewidth=2,
                    linestyle="--",
                    label="Kel Fit",
                )

        handles, labels = (
            self.axes.get_legend_handles_labels()
        )

        if handles:
            self.axes.legend()
        self.draw()