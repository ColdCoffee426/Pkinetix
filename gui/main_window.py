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

        self.statusBar().showMessage("Ready")

    def _create_central_widget(self) -> None:
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

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
        results_panel = self._create_panel(
            "Results",
            self.results,
        )
        table_panel = self._create_panel(
            "Concentration-Time Data",
            self.data_table,
        )

        for panel in (
            study_panel,
            graph_panel,
            results_panel,
        ):
            panel.setMinimumHeight(0)
            panel.setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Ignored,
            )

        table_panel.setMinimumHeight(120)
        table_panel.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding,
        )

        self.top_splitter = QSplitter(Qt.Horizontal)
        self.top_splitter.addWidget(study_panel)
        self.top_splitter.addWidget(graph_panel)
        self.top_splitter.addWidget(results_panel)
        self.top_splitter.setStretchFactor(0, 2)
        self.top_splitter.setStretchFactor(1, 6)
        self.top_splitter.setStretchFactor(2, 2)
        self.top_splitter.setChildrenCollapsible(False)
        self.top_splitter.setSizes([280, 800, 320])
        self.top_splitter.setMinimumHeight(0)
        self.top_splitter.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Ignored,
        )
        self.top_splitter.setHandleWidth(6)

        self.main_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.addWidget(self.top_splitter)
        self.main_splitter.addWidget(table_panel)
        self.main_splitter.setStretchFactor(0, 2)
        self.main_splitter.setStretchFactor(1, 1)
        self.main_splitter.setChildrenCollapsible(True)
        self.main_splitter.setCollapsible(0, True)
        self.main_splitter.setCollapsible(1, False)
        self.main_splitter.setSizes([540, 340])
        self.main_splitter.setHandleWidth(8)

        self.main_layout.addWidget(self.main_splitter)

        study_panel.setMinimumWidth(260)
        graph_panel.setMinimumWidth(450)
        results_panel.setMinimumWidth(240)

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
        layout.setContentsMargins(8, 12, 8, 8)
        layout.addWidget(widget)

        return panel

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