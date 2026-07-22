from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QWidget,
)


class StudyInformationWidget(QWidget):
    """
    Collects project, dosing and analysis information.
    """

    data_changed = Signal()

    def __init__(self) -> None:
        super().__init__()

        layout = QFormLayout(self)

        self.study_name = QLineEdit()
        self.drug_name = QLineEdit()
        self.subject_id = QLineEdit()
        self.dose = QLineEdit()
        self.body_weight = QLineEdit()

        self.route = QComboBox()
        self.route.addItem("Oral", "Oral")
        self.route.addItem("IV Bolus", "IV Bolus")
        self.route.addItem("IV Infusion", "IV Infusion")
        self.route.addItem("IM", "IM")
        self.route.addItem("SC", "SC")

        self.auc_method = QComboBox()
        self.auc_method.addItem(
            "Linear-Up / Log-Down",
            "linear_up_log_down",
        )
        self.auc_method.addItem(
            "Linear Trapezoidal",
            "linear",
        )
        self.auc_method.addItem(
            "Log Trapezoidal",
            "log",
        )

        self.comments = QTextEdit()

        layout.addRow("Study Name", self.study_name)
        layout.addRow("Drug Name", self.drug_name)
        layout.addRow("Subject ID", self.subject_id)
        layout.addRow("Dose", self.dose)
        layout.addRow("Route", self.route)
        layout.addRow("AUC Method", self.auc_method)
        layout.addRow("Body Weight", self.body_weight)
        layout.addRow("Comments", self.comments)

        self.study_name.textChanged.connect(self.data_changed)
        self.drug_name.textChanged.connect(self.data_changed)
        self.subject_id.textChanged.connect(self.data_changed)
        self.dose.textChanged.connect(self.data_changed)
        self.body_weight.textChanged.connect(self.data_changed)
        self.route.currentIndexChanged.connect(self.data_changed)
        self.auc_method.currentIndexChanged.connect(
            self.data_changed
        )
        self.comments.textChanged.connect(self.data_changed)

    def get_data(self) -> dict[str, str]:
        """
        Return the current study and analysis information.
        """

        return {
            "study_name": self.study_name.text().strip(),
            "drug_name": self.drug_name.text().strip(),
            "subject_id": self.subject_id.text().strip(),
            "dose": self.dose.text().strip(),
            "body_weight": self.body_weight.text().strip(),
            "route": str(self.route.currentData()),
            "auc_method": str(self.auc_method.currentData()),
            "comments": self.comments.toPlainText().strip(),
        }