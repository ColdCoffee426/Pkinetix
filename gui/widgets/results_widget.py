from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.models.analysis_result import AnalysisResult
from app.models.units import Units


class ResultsWidget(QWidget):
    """Displays calculated pharmacokinetic parameters."""

    def __init__(self) -> None:
        super().__init__()
        self.labels: dict[str, QLabel] = {}
        self.title_labels: dict[str, QLabel] = {}
        self.base_titles: dict[str, str] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        heading = QLabel("OUTPUT")
        heading.setObjectName("majorHeading")
        heading.setAlignment(Qt.AlignCenter)
        heading.setFixedHeight(36)
        layout.addWidget(heading)

        section_heading = QLabel("Pharmacokinetic Parameters")
        section_heading.setObjectName("sectionHeading")
        section_heading.setAlignment(Qt.AlignCenter)
        section_heading.setFixedHeight(36)
        layout.addWidget(section_heading)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 6, 10, 10)
        content_layout.setSpacing(0)
        content_layout.setAlignment(Qt.AlignTop)

        parameters = [
            ("C<sub>max</sub>", "cmax"),
            ("T<sub>max</sub>", "tmax"),
            ("AUC<sub>0-t</sub>", "auc_0_t"),
            ("AUC<sub>Extrapolated</sub>", "auc_extrapolated"),
            ("AUC<sub>0-∞</sub>", "auc_0_inf"),
            ("Sample Adequacy","auc_extrapolated_percent",),
            ("AUMC<sub>0-t</sub>", "aumc"),
            ("AUMC<sub>Extrapolated</sub>", "aumc_extrapolated"),
            ("AUMC<sub>0-∞", "aumc_0_inf"),
            ("MRT", "mrt"),
            ("Vd", "vz"),
            ("V<sub>d</sub>/kg", "vd_per_kg"),
            ("K<sub>el</sub>", "lambda_z"),
            ("Half-life", "t_half"),
            ("Clearance", "cl"),
        ]

        for index, parameter in enumerate(parameters):
            content_layout.addWidget(self._create_result_row(*parameter))
            if index < len(parameters) - 1:
                content_layout.addWidget(self._create_separator())

        scroll_area.setWidget(content)
        layout.addWidget(scroll_area)
        self.update_units(Units())

    def _create_result_row(self, title: str, attribute: str) -> QWidget:
        row_widget = QWidget()
        row_widget.setObjectName("resultRow")
        layout = QGridLayout(row_widget)
        layout.setContentsMargins(4, 6, 4, 6)
        layout.setHorizontalSpacing(10)
        layout.setColumnStretch(0, 4)
        layout.setColumnStretch(1, 2)

        title_label = QLabel(title)
        title_label.setTextFormat(Qt.RichText)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        value_label = QLabel("--")
        value_label.setObjectName("plainResultValue")
        value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        value_label.setMinimumWidth(95)

        self.base_titles[attribute] = title
        self.title_labels[attribute] = title_label
        self.labels[attribute] = value_label

        layout.addWidget(title_label, 0, 0)
        layout.addWidget(value_label, 0, 1)
        return row_widget

    @staticmethod
    def _create_separator() -> QFrame:
        line = QFrame()
        line.setObjectName("resultSeparator")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        line.setFixedHeight(1)
        return line

    def update_units(self, units: Units) -> None:
        unit_map = {
            "cmax": units.concentration,
            "tmax": units.time,
            "auc_0_t": units.auc,
            "auc_extrapolated": units.auc,
            "auc_0_inf": units.auc,
            "auc_extrapolated_percent": "%",
            "aumc": units.aumc,
            "aumc_extrapolated": units.aumc,
            "aumc_0_inf": units.aumc,
            "mrt": units.time,
            "vz": units.volume,
            "vd_per_kg": f"{units.volume}/kg",
            "lambda_z": f"1/{units.time}",
            "t_half": units.time,
            "cl": units.clearance,
        }

        for attribute, title_label in self.title_labels.items():
            unit = unit_map.get(attribute, "")
            base_title = self.base_titles[attribute]
            title_label.setText(
                f"{base_title} ({unit})" if unit else base_title
            )

    def clear_results(self) -> None:
        for label in self.labels.values():
            label.setText("--")

    def update_results(self, results: AnalysisResult) -> None:
        for attribute, label in self.labels.items():
            value = getattr(results, attribute, None)
            if value is None:
                label.setText("--")
            elif isinstance(value, float):
                label.setText(f"{value:.4f}")
            else:
                label.setText(str(value))


class GoodnessOfFitWidget(QWidget):
    """Displays terminal-phase fit statistics."""

    def __init__(self) -> None:
        super().__init__()
        self.labels: dict[str, QLabel] = {}
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        heading = QLabel("Goodness of Fit Statistical Criteria")
        heading.setObjectName("majorHeading")
        heading.setAlignment(Qt.AlignCenter)
        heading.setFixedHeight(36)
        layout.addWidget(heading)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 5, 10, 8)
        content_layout.setSpacing(0)

        statistics = [
            ("R²", "terminal_r_squared"),
            ("Adjusted R²", "terminal_adjusted_r_squared"),
            ("Confidence", "terminal_confidence"),
            ("AIC", "terminal_aic"),
            ("Bias", "terminal_bias"),
            ("BIC", "terminal_bic"),
            ("SSE", "terminal_sse"),
            ("RMSE", "terminal_rmse"),
            ("MAE", "terminal_mae"),
        ]

        for row_index in range(0, len(statistics), 3):
            row_widget = QWidget()
            row_layout = QGridLayout(row_widget)
            row_layout.setContentsMargins(4, 6, 4, 6)
            row_layout.setHorizontalSpacing(10)

            for index, (title, attribute) in enumerate(
                statistics[row_index:row_index + 3]
            ):
                title_column = index * 2
                value_column = title_column + 1
                title_label = QLabel(title)
                value_label = QLabel("--")
                value_label.setObjectName("plainResultValue")
                value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                value_label.setMinimumWidth(75)
                self.labels[attribute] = value_label
                row_layout.addWidget(title_label, 0, title_column)
                row_layout.addWidget(value_label, 0, value_column)
                row_layout.setColumnStretch(title_column, 1)

            content_layout.addWidget(row_widget)
            if row_index + 3 < len(statistics):
                content_layout.addWidget(ResultsWidget._create_separator())

        layout.addWidget(content)

    def clear_results(self) -> None:
        for label in self.labels.values():
            label.setText("--")

    def update_results(self, results: AnalysisResult) -> None:
        for attribute, label in self.labels.items():
            value = getattr(results, attribute, None)
            if value is None:
                label.setText("--")
            elif isinstance(value, float):
                label.setText(f"{value:.4f}")
            else:
                label.setText(str(value))
