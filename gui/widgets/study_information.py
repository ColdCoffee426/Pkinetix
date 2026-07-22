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
    Collects project and dosing information.
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
        self.route.addItems([
            "Oral",
            "IV Bolus",
            "IV Infusion",
            "IM",
            "SC",
        ])

        self.comments = QTextEdit()

        layout.addRow("Study Name", self.study_name)
        layout.addRow("Drug Name", self.drug_name)
        layout.addRow("Subject ID", self.subject_id)
        layout.addRow("Dose", self.dose)
        layout.addRow("Route", self.route)
        layout.addRow("Body Weight", self.body_weight)
        layout.addRow("Comments", self.comments)

        self.study_name.textChanged.connect(self.data_changed)
        self.drug_name.textChanged.connect(self.data_changed)
        self.subject_id.textChanged.connect(self.data_changed)
        self.dose.textChanged.connect(self.data_changed)
        self.body_weight.textChanged.connect(self.data_changed)
        self.route.currentTextChanged.connect(self.data_changed)
        self.comments.textChanged.connect(self.data_changed)

    def get_data(self) -> dict[str, str]:
        """
        Return the current study information.
        """

        return {
            "study_name": self.study_name.text().strip(),
            "drug_name": self.drug_name.text().strip(),
            "subject_id": self.subject_id.text().strip(),
            "dose": self.dose.text().strip(),
            "body_weight": self.body_weight.text().strip(),
            "route": self.route.currentText(),
            "comments": self.comments.toPlainText().strip(),
        }