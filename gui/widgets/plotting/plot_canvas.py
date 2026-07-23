import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter
from scipy.interpolate import PchipInterpolator


class PlotCanvas(FigureCanvasQTAgg):
    """
    Matplotlib canvas for observed data, smooth profile and terminal fit.
    """

    def __init__(self) -> None:
        self.figure = Figure(figsize=(3, 4), tight_layout=True)
        super().__init__(self.figure)
        self.axes = self.figure.add_subplot(111)
        self.scale_mode = "log"
        self._configure_axes()

    def _configure_axes(self) -> None:
        self.axes.set_title("Concentration-Time Profile")
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Concentration")

        if self.scale_mode == "log":
            self.axes.set_yscale("log")
            self.axes.yaxis.set_major_locator(LogLocator(base=10.0))
            self.axes.yaxis.set_minor_locator(
                LogLocator(base=10.0, subs=tuple(range(2, 10)))
            )
            self.axes.yaxis.set_major_formatter(
                FuncFormatter(lambda value, _: f"{value:g}")
            )
            self.axes.yaxis.set_minor_formatter(NullFormatter())
            self.axes.grid(True, which="major", linewidth=0.9)
            self.axes.grid(True, which="minor", linewidth=0.35, alpha=0.55)
        else:
            self.axes.set_yscale("linear")
            self.axes.grid(True, which="major", linewidth=0.8)

    def set_scale_mode(self, mode: str) -> None:
        if mode not in ("linear", "log"):
            raise ValueError("Graph scale must be linear or log.")
        self.scale_mode = mode

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

        valid_pairs = [
            (t, c)
            for t, c in zip(time, concentration)
            if self.scale_mode != "log" or c > 0
        ]

        if valid_pairs:
            observed_time = [pair[0] for pair in valid_pairs]
            observed_concentration = [pair[1] for pair in valid_pairs]

            self.axes.scatter(
                observed_time,
                observed_concentration,
                s=38,
                label="Observed",
                zorder=4,
            )

            if len(valid_pairs) >= 3 and len(set(observed_time)) == len(observed_time):
                dense_time = np.linspace(
                    min(observed_time),
                    max(observed_time),
                    240,
                )
                curve = PchipInterpolator(
                    observed_time,
                    observed_concentration,
                )(dense_time)

                if self.scale_mode == "log":
                    mask = curve > 0
                    dense_time = dense_time[mask]
                    curve = curve[mask]

                self.axes.plot(
                    dense_time,
                    curve,
                    linewidth=2,
                    label="Profile Curve",
                )

        if highlighted_time and highlighted_concentration:
            terminal_pairs = [
                (t, c)
                for t, c in zip(highlighted_time, highlighted_concentration)
                if self.scale_mode != "log" or c > 0
            ]
            if terminal_pairs:
                self.axes.scatter(
                    [pair[0] for pair in terminal_pairs],
                    [pair[1] for pair in terminal_pairs],
                    s=68,
                    label="Terminal Phase",
                    zorder=5,
                )

        if fitted_time and fitted_concentration:
            terminal_fit = [
                (t, c)
                for t, c in zip(fitted_time, fitted_concentration)
                if self.scale_mode != "log" or c > 0
            ]
            if terminal_fit:
                self.axes.plot(
                    [pair[0] for pair in terminal_fit],
                    [pair[1] for pair in terminal_fit],
                    linewidth=2,
                    linestyle="-",
                    label="Kel Fit",
                )

        handles, _ = self.axes.get_legend_handles_labels()
        if handles:
            self.axes.legend()

        self.draw()
