from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.models.analysis_result import AnalysisResult


class ResultsWidget(QWidget):
    """
    Displays PK results in a horizontal table.
    """

    def __init__(self) -> None:
        super().__init__()

        self.parameters = [
            ("Cmax", "cmax"),
            ("Tmax", "tmax"),
            ("λz", "lambda_z"),
            ("Half-life", "t_half"),
            ("AUC₀-t", "auc_0_t"),
            ("AUC₀-∞", "auc_0_inf"),
            ("AUC Extrap.", "auc_extrapolated"),
            ("% Extrap.", "auc_extrapolated_percent"),
            ("AUMC", "aumc"),
            ("MRT", "mrt"),
            ("Clearance", "cl"),
            ("Vz", "vz"),
            ("Terminal R²", "terminal_r_squared"),
            ("Adjusted R²", "terminal_adjusted_r_squared"),
            ("SSE", "terminal_sse"),
            ("AIC", "terminal_aic"),
            ("BIC", "terminal_bic"),
            ("RMSE", "terminal_rmse"),
            ("MAE", "terminal_mae"),
            ("Bias", "terminal_bias"),
            ("Confidence", "terminal_confidence"),
        ]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget(
            1,
            len(self.parameters),
        )
        self.table.setHorizontalHeaderLabels([
            title for title, _ in self.parameters
        ])
        self.table.setVerticalHeaderLabels(["Value"])
        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectItems
        )
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.setWordWrap(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        header.setStretchLastSection(False)
        header.setDefaultAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )

        self.table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        for column in range(len(self.parameters)):
            item = QTableWidgetItem("--")
            item.setTextAlignment(
                Qt.AlignLeft | Qt.AlignVCenter
            )
            self.table.setItem(0, column, item)

        layout.addWidget(self.table)

    def clear_results(self) -> None:
        """
        Reset all displayed values.
        """

        for column in range(len(self.parameters)):
            self.table.item(0, column).setText("--")

    def update_results(
        self,
        results: AnalysisResult,
    ) -> None:
        """
        Display calculated PK results.
        """

        for column, (_, attribute) in enumerate(
            self.parameters
        ):
            value = getattr(results, attribute, None)

            if value is None:
                text = "--"
            elif isinstance(value, float):
                text = f"{value:.4f}"
            else:
                text = str(value)

            self.table.item(0, column).setText(text)