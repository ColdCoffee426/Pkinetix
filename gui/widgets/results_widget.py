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
    """
    Displays calculated pharmacokinetic parameters.
    """

    def __init__(self) -> None:
        super().__init__()

        self.labels: dict[str, QLabel] = {}
        self.unit_labels: dict[str, QLabel] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        heading = QLabel("OUTPUT")
        heading.setObjectName("majorHeading")
        heading.setAlignment(Qt.AlignCenter)
        heading.setFixedHeight(36)
        layout.addWidget(heading)

        section_heading = QLabel(
            "Pharmacokinetic Parameters"
        )
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
            ("Cmax", "cmax"),
            ("Tmax", "tmax"),
            ("AUC 0-t", "auc_0_t"),
            ("AUC Extrapolated", "auc_extrapolated"),
            ("AUC 0-inf", "auc_0_inf"),
            (
                "Sample Adequacy Factor",
                "auc_extrapolated_percent",
            ),
            ("AUMC 0-t", "aumc"),
            ("AUMC Extrapolated", "aumc_extrapolated"),
            ("AUMC 0-inf", "aumc_0_inf"),
            ("MRT", "mrt"),
            ("Vd", "vz"),
            ("Vd/kg", "vd_per_kg"),
            ("K<sub>el</sub>", "lambda_z"),
            ("Half-life", "t_half"),
            ("Clearance", "cl"),
        ]

        for index, parameter in enumerate(parameters):
            content_layout.addWidget(
                self._create_result_row(*parameter)
            )

            if index < len(parameters) - 1:
                content_layout.addWidget(
                    self._create_separator()
                )

        scroll_area.setWidget(content)
        layout.addWidget(scroll_area)

        self.update_units(Units())

    def _create_result_row(
        self,
        title: str,
        attribute: str,
    ) -> QWidget:
        row_widget = QWidget()
        row_widget.setObjectName("resultRow")

        layout = QGridLayout(row_widget)
        layout.setContentsMargins(4, 6, 4, 6)
        layout.setHorizontalSpacing(8)

        layout.setColumnStretch(0, 5)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)

        title_label = QLabel(title)
        title_label.setTextFormat(Qt.RichText)
        title_label.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )

        value_label = QLabel("--")
        value_label.setObjectName("plainResultValue")
        value_label.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        value_label.setMinimumWidth(72)
        value_label.setMaximumWidth(105)

        unit_label = QLabel("")
        unit_label.setObjectName("resultUnit")
        unit_label.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )
        unit_label.setMinimumWidth(64)

        self.labels[attribute] = value_label
        self.unit_labels[attribute] = unit_label

        layout.addWidget(title_label, 0, 0)
        layout.addWidget(value_label, 0, 1)
        layout.addWidget(unit_label, 0, 2)

        return row_widget

    @staticmethod
    def _create_separator() -> QFrame:
        line = QFrame()
        line.setObjectName("resultSeparator")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        line.setFixedHeight(1)
        return line

    def update_units(
        self,
        units: Units,
    ) -> None:
        """
        Update displayed units after unit selection changes.
        """

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

        for attribute, label in self.unit_labels.items():
            label.setText(unit_map.get(attribute, ""))

    def clear_results(self) -> None:
        for label in self.labels.values():
            label.setText("--")

    def update_results(
        self,
        results: AnalysisResult,
    ) -> None:
        for attribute, label in self.labels.items():
            value = getattr(results, attribute, None)

            if value is None:
                label.setText("--")
            elif isinstance(value, float):
                label.setText(f"{value:.4f}")
            else:
                label.setText(str(value))


class GoodnessOfFitWidget(QWidget):
    """
    Displays terminal-phase fit statistics.
    """

    def __init__(self) -> None:
        super().__init__()

        self.labels: dict[str, QLabel] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        heading = QLabel(
            "Goodness of Fit Statistical Criteria"
        )
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

        rows = [
            statistics[index:index + 3]
            for index in range(0, len(statistics), 3)
        ]

        for row_index, row_items in enumerate(rows):
            row_widget = QWidget()
            row_layout = QGridLayout(row_widget)
            row_layout.setContentsMargins(4, 6, 4, 6)
            row_layout.setHorizontalSpacing(10)

            for index, (title, attribute) in enumerate(
                row_items
            ):
                title_column = index * 2
                value_column = title_column + 1

                title_label = QLabel(title)

                value_label = QLabel("--")
                value_label.setObjectName(
                    "plainResultValue"
                )
                value_label.setAlignment(
                    Qt.AlignRight | Qt.AlignVCenter
                )
                value_label.setMinimumWidth(75)

                self.labels[attribute] = value_label

                row_layout.addWidget(
                    title_label,
                    0,
                    title_column,
                )
                row_layout.addWidget(
                    value_label,
                    0,
                    value_column,
                )

                row_layout.setColumnStretch(
                    title_column,
                    1,
                )

            content_layout.addWidget(row_widget)

            if row_index < len(rows) - 1:
                content_layout.addWidget(
                    ResultsWidget._create_separator()
                )

        layout.addWidget(content)

    def clear_results(self) -> None:
        for label in self.labels.values():
            label.setText("--")

    def update_results(
        self,
        results: AnalysisResult,
    ) -> None:
        for attribute, label in self.labels.items():
            value = getattr(results, attribute, None)

            if value is None:
                label.setText("--")
            elif isinstance(value, float):
                label.setText(f"{value:.4f}")
            else:
                label.setText(str(value))