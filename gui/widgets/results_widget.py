from PySide6.QtWidgets import QFormLayout, QLabel, QWidget

from app.models.analysis_result import AnalysisResult


class ResultsWidget(QWidget):
    """
    Displays pharmacokinetic analysis results.
    """

    def __init__(self) -> None:
        super().__init__()

        self.labels: dict[str, QLabel] = {}
        layout = QFormLayout(self)

        parameters = [
            ("Cmax", "cmax"),
            ("Tmax", "tmax"),
            ("λz", "lambda_z"),
            ("Half-life", "t_half"),
            ("AUC₀-t", "auc_0_t"),
            ("AUC₀-∞", "auc_0_inf"),
            ("AUC Extrap.", "auc_extrapolated"),
            ("% AUC Extrap.", "auc_extrapolated_percent"),
            ("AUMC", "aumc"),
            ("MRT", "mrt"),
            ("Clearance", "cl"),
            ("Vz", "vz"),
            ("Terminal R²", "terminal_r_squared"),
            ("Adjusted R²", "terminal_adjusted_r_squared"),
            ("Terminal SSE", "terminal_sse"),
            ("Terminal AIC", "terminal_aic"),
            ("Terminal BIC", "terminal_bic"),
            ("Terminal RMSE", "terminal_rmse"),
            ("Terminal MAE", "terminal_mae"),
            ("Terminal Bias", "terminal_bias"),
            ("Confidence", "terminal_confidence"),
        ]

        for title, attribute in parameters:
            label = QLabel("--")
            self.labels[attribute] = label
            layout.addRow(title, label)

    def clear_results(self) -> None:
        """
        Reset all displayed values.
        """

        for label in self.labels.values():
            label.setText("--")

    def update_results(
        self,
        results: AnalysisResult,
    ) -> None:
        """
        Update displayed pharmacokinetic results.
        """

        for attribute, label in self.labels.items():
            value = getattr(
                results,
                attribute,
                None,
            )

            if value is None:
                label.setText("--")
            elif isinstance(value, float):
                label.setText(f"{value:.4f}")
            else:
                label.setText(str(value))