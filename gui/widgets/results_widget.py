from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.models.analysis_result import AnalysisResult


class ResultsWidget(QWidget):
    """
    Displays calculated pharmacokinetic parameters.
    """

    def __init__(self) -> None:
        super().__init__()

        self.labels: dict[str, QLabel] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        heading = QLabel("OUTPUT")
        heading.setObjectName("majorHeading")
        heading.setAlignment(Qt.AlignCenter)
        heading.setMinimumHeight(34)
        layout.addWidget(heading)

        section_heading = QLabel(
            "Pharmacokinetic Parameters"
        )
        section_heading.setObjectName("sectionHeading")
        section_heading.setAlignment(Qt.AlignCenter)
        section_heading.setMinimumHeight(30)
        layout.addWidget(section_heading)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(8, 8, 8, 8)
        content_layout.setAlignment(Qt.AlignTop)

        parameters = [
            ("Cmax", "cmax"),
            ("Tmax", "tmax"),
            ("AUC 0-t", "auc_0_t"),
            ("AUC Extrapolated", "auc_extrapolated"),
            ("AUC 0-inf", "auc_0_inf"),
            (
                "Sample Adequacy Factor (%)",
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

        content_layout.addLayout(
            self._create_result_grid(parameters)
        )

        scroll_area.setWidget(content)
        layout.addWidget(scroll_area)

    def _create_result_grid(
        self,
        parameters: list[tuple[str, str]],
    ) -> QGridLayout:
        layout = QGridLayout()
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(5)
        layout.setColumnStretch(0, 1)

        for row, (title, attribute) in enumerate(parameters):
            title_label = QLabel(title)
            title_label.setTextFormat(Qt.RichText)
            title_label.setAlignment(
                Qt.AlignLeft | Qt.AlignVCenter
            )

            value_label = QLabel("--")
            value_label.setObjectName("resultValue")
            value_label.setAlignment(
                Qt.AlignRight | Qt.AlignVCenter
            )
            value_label.setMinimumWidth(95)

            self.labels[attribute] = value_label

            layout.addWidget(title_label, row, 0)
            layout.addWidget(value_label, row, 1)

        return layout

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
        heading.setMinimumHeight(34)
        layout.addWidget(heading)

        content = QWidget()
        grid = QGridLayout(content)
        grid.setContentsMargins(10, 8, 10, 8)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(6)

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

        columns = 3

        for index, (title, attribute) in enumerate(
            statistics
        ):
            row = index // columns
            column = (index % columns) * 2

            title_label = QLabel(title)
            title_label.setAlignment(
                Qt.AlignLeft | Qt.AlignVCenter
            )

            value_label = QLabel("--")
            value_label.setObjectName("resultValue")
            value_label.setAlignment(
                Qt.AlignRight | Qt.AlignVCenter
            )
            value_label.setMinimumWidth(90)

            self.labels[attribute] = value_label

            grid.addWidget(title_label, row, column)
            grid.addWidget(
                value_label,
                row,
                column + 1,
            )

        for column in range(columns * 2):
            if column % 2 == 0:
                grid.setColumnStretch(column, 1)

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