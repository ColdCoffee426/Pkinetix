from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QComboBox
)


class StudyInformationWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QFormLayout()

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
            "SC"
        ])

        self.comments = QTextEdit()

        layout.addRow("Study Name", self.study_name)
        layout.addRow("Drug Name", self.drug_name)
        layout.addRow("Subject ID", self.subject_id)
        layout.addRow("Dose", self.dose)
        layout.addRow("Route", self.route)
        layout.addRow("Body Weight", self.body_weight)
        layout.addRow("Comments", self.comments)

        self.setLayout(layout)