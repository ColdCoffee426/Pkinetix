from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGroupBox,
    QMainWindow,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.controllers.project_controller import ProjectController
from app.state.application_state import ApplicationState
from gui.widgets.data_table import DataTableWidget
from gui.widgets.graph_widget import GraphWidget
from gui.widgets.results_widget import ResultsWidget
from gui.widgets.study_information import StudyInformationWidget
from pk.analysis_engine import AnalysisEngine


class MainWindow(QMainWindow):
    """
    Main application window for PKinetix.
    """

    def __init__(self) -> None:
        super().__init__()

        self.application_state = ApplicationState()
        self.project_controller = ProjectController(
            self.application_state.project
        )
        self.analysis_engine = AnalysisEngine(
            self.application_state.project
        )

        self.setWindowTitle("PKinetix")
        self.resize(1400, 900)

        self._create_central_widget()
        self._create_layout()
        self._connect_signals()
        self._apply_theme()

        self.statusBar().showMessage("Ready")

    def _create_central_widget(self) -> None:
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(
            self.central_widget
        )
        self.main_layout.setContentsMargins(6, 6, 6, 6)

    def _create_layout(self) -> None:
        self.study_information = StudyInformationWidget()
        self.graph = GraphWidget()
        self.results = ResultsWidget()
        self.data_table = DataTableWidget()

        study_panel = self._create_panel(
            "Study Information",
            self.study_information,
        )
        graph_panel = self._create_panel(
            "Concentration-Time Plot",
            self.graph,
        )
        table_panel = self._create_panel(
            "Concentration-Time Data",
            self.data_table,
        )
        results_panel = self._create_panel(
            "Results",
            self.results,
        )

        study_panel.setMinimumWidth(250)
        graph_panel.setMinimumWidth(420)
        table_panel.setMinimumWidth(340)

        for panel in (
            study_panel,
            graph_panel,
            table_panel,
        ):
            panel.setMinimumHeight(0)
            panel.setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Expanding,
            )

        results_panel.setMinimumHeight(120)
        results_panel.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        self.top_splitter = QSplitter(Qt.Horizontal)
        self.top_splitter.addWidget(study_panel)
        self.top_splitter.addWidget(graph_panel)
        self.top_splitter.addWidget(table_panel)
        self.top_splitter.setStretchFactor(0, 2)
        self.top_splitter.setStretchFactor(1, 5)
        self.top_splitter.setStretchFactor(2, 3)
        self.top_splitter.setChildrenCollapsible(False)
        self.top_splitter.setSizes([270, 700, 430])
        self.top_splitter.setHandleWidth(7)

        self.main_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.addWidget(self.top_splitter)
        self.main_splitter.addWidget(results_panel)
        self.main_splitter.setStretchFactor(0, 7)
        self.main_splitter.setStretchFactor(1, 3)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setSizes([650, 230])
        self.main_splitter.setHandleWidth(8)

        self.main_layout.addWidget(self.main_splitter)

    def _connect_signals(self) -> None:
        self.data_table.data_changed.connect(
            self._on_data_changed
        )
        self.study_information.data_changed.connect(
            self._on_study_information_changed
        )
        self.project_controller.project_changed.connect(
            self._project_changed
        )

    def _create_panel(
        self,
        title: str,
        widget: QWidget,
    ) -> QGroupBox:
        panel = QGroupBox(title)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 14, 8, 8)
        layout.addWidget(widget)

        return panel

    def _apply_theme(self) -> None:
        """
        Apply the PKinetix teal-blue interface theme.
        """

        self.setStyleSheet("""
            QMainWindow,
            QWidget {
                background-color: #17242b;
                color: #dbe7eb;
                font-size: 13px;
            }

            QGroupBox {
                background-color: #1d3038;
                border: 1px solid #2f6671;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 7px;
                font-weight: 600;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
                color: #80d0d4;
                background-color: #1d3038;
            }

            QLineEdit,
            QTextEdit,
            QComboBox {
                background-color: #223942;
                color: #e6f1f3;
                border: 1px solid #356c78;
                border-radius: 4px;
                padding: 5px;
                selection-background-color: #236d83;
            }

            QLineEdit:focus,
            QTextEdit:focus,
            QComboBox:focus {
                border: 1px solid #54b8c1;
            }

            QComboBox QAbstractItemView {
                background-color: #223942;
                color: #e6f1f3;
                selection-background-color: #245f7a;
            }

            QTableWidget {
                background-color: #1b2d35;
                alternate-background-color: #203842;
                color: #e2edf0;
                gridline-color: #365d68;
                border: 1px solid #315e69;
                selection-background-color: #245f7a;
                selection-color: #ffffff;
            }

            QHeaderView::section {
                background-color: #214d5b;
                color: #e7f4f5;
                border: 1px solid #387381;
                padding: 6px;
                font-weight: 600;
            }

            QTableCornerButton::section {
                background-color: #214d5b;
                border: 1px solid #387381;
            }

            QSplitter::handle {
                background-color: #28566a;
            }

            QSplitter::handle:hover {
                background-color: #3c8191;
            }

            QScrollBar:vertical,
            QScrollBar:horizontal {
                background-color: #172a32;
                border: none;
            }

            QScrollBar::handle {
                background-color: #356c78;
                border-radius: 4px;
                min-width: 20px;
                min-height: 20px;
            }

            QScrollBar::handle:hover {
                background-color: #438ba0;
            }

            QScrollBar::add-line,
            QScrollBar::sub-line {
                width: 0;
                height: 0;
            }

            QStatusBar {
                background-color: #15313f;
                color: #9dd7df;
                border-top: 1px solid #2e6370;
            }

            QLabel {
                background-color: transparent;
            }
        """)

    def _on_data_changed(self) -> None:
        data = self.data_table.get_data()
        self.project_controller.update_observations(data)

    def _on_study_information_changed(self) -> None:
        data = self.study_information.get_data()
        self.project_controller.update_study_information(data)

    def _project_changed(self) -> None:
        time, concentration = (
            self.analysis_engine.get_plot_data()
        )

        results = self.project_controller.analysis_result

        if results is None:
            self.graph.plot_profile(
                time,
                concentration,
            )
            self.results.clear_results()
        else:
            self.graph.plot_profile(
                time,
                concentration,
                fitted_time=results.fitted_terminal_times,
                fitted_concentration=(
                    results.fitted_terminal_concentrations
                ),
                highlighted_time=results.terminal_times,
                highlighted_concentration=(
                    results.terminal_concentrations
                ),
            )
            self.results.update_results(results)

        self.statusBar().showMessage(
            f"{len(time)} observations loaded"
        )