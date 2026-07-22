from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QWidget,
)


class StudyInformationWidget(QWidget):
    """
    Collects project, dosing and unit information.
    """

    data_changed = Signal()
    time_unit_changed = Signal(str, str)
    concentration_unit_changed = Signal(str, str)

    def __init__(self) -> None:
        super().__init__()

        self._previous_time_unit = "h"
        self._previous_concentration_unit = "ng/mL"

        layout = QGridLayout(self)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 0)

        self.study_name = QLineEdit()
        self.drug_name = QLineEdit()
        self.subject_id = QLineEdit()
        self.dose = QLineEdit()
        self.body_weight = QLineEdit()
        self.comments = QTextEdit()
        self.comments.setMaximumHeight(75)

        self.dose_unit = QComboBox()
        self.dose_unit.addItem("mg", "mg")

        self.concentration_unit = QComboBox()
        self.concentration_unit.addItem("ng/mL", "ng/mL")
        self.concentration_unit.addItem("µg/mL", "µg/mL")

        self.time_unit = QComboBox()
        self.time_unit.addItem("Hours", "h")
        self.time_unit.addItem("Minutes", "min")

        self.body_weight_unit = QComboBox()
        self.body_weight_unit.addItem("kg", "kg")

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

        layout.addWidget(QLabel("Study Name"), 0, 0)
        layout.addWidget(self.study_name, 0, 1, 1, 2)

        layout.addWidget(QLabel("Drug Name"), 1, 0)
        layout.addWidget(self.drug_name, 1, 1, 1, 2)

        layout.addWidget(QLabel("Subject ID"), 2, 0)
        layout.addWidget(self.subject_id, 2, 1, 1, 2)

        layout.addWidget(QLabel("Dose"), 3, 0)
        layout.addWidget(self.dose, 3, 1)
        layout.addWidget(self.dose_unit, 3, 2)

        layout.addWidget(QLabel("Concentration Unit"), 4, 0)
        layout.addWidget(self.concentration_unit, 4, 1, 1, 2)

        layout.addWidget(QLabel("Time Unit"), 5, 0)
        layout.addWidget(self.time_unit, 5, 1, 1, 2)

        layout.addWidget(QLabel("Route"), 6, 0)
        layout.addWidget(self.route, 6, 1, 1, 2)

        layout.addWidget(QLabel("AUC Method"), 7, 0)
        layout.addWidget(self.auc_method, 7, 1, 1, 2)

        layout.addWidget(QLabel("Body Weight"), 8, 0)
        layout.addWidget(self.body_weight, 8, 1)
        layout.addWidget(self.body_weight_unit, 8, 2)

        layout.addWidget(QLabel("Remarks"), 9, 0)
        layout.addWidget(self.comments, 9, 1, 1, 2)

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

        self.time_unit.currentIndexChanged.connect(
            self._on_time_unit_changed
        )
        self.concentration_unit.currentIndexChanged.connect(
            self._on_concentration_unit_changed
        )

    def _on_time_unit_changed(self) -> None:
        new_unit = str(self.time_unit.currentData())
        old_unit = self._previous_time_unit

        if new_unit != old_unit:
            self._previous_time_unit = new_unit
            self.time_unit_changed.emit(old_unit, new_unit)
            self.data_changed.emit()

    def _on_concentration_unit_changed(self) -> None:
        new_unit = str(self.concentration_unit.currentData())
        old_unit = self._previous_concentration_unit

        if new_unit != old_unit:
            self._previous_concentration_unit = new_unit
            self.concentration_unit_changed.emit(
                old_unit,
                new_unit,
            )
            self.data_changed.emit()

    def get_data(self) -> dict[str, str]:
        """
        Return current study, dosing and unit information.
        """

        return {
            "study_name": self.study_name.text().strip(),
            "drug_name": self.drug_name.text().strip(),
            "subject_id": self.subject_id.text().strip(),
            "dose": self.dose.text().strip(),
            "dose_unit": str(self.dose_unit.currentData()),
            "concentration_unit": str(
                self.concentration_unit.currentData()
            ),
            "time_unit": str(self.time_unit.currentData()),
            "body_weight": self.body_weight.text().strip(),
            "body_weight_unit": str(
                self.body_weight_unit.currentData()
            ),
            "route": str(self.route.currentData()),
            "auc_method": str(self.auc_method.currentData()),
            "comments": self.comments.toPlainText().strip(),
        }