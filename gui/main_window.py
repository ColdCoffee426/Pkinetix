from PySide6.QtCore import Qt
from pk.analysis_engine import AnalysisEngine
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSplitter,
    QToolBar,
    QGroupBox,
)




from gui.widgets.study_information import StudyInformationWidget
from gui.widgets.data_table import DataTableWidget
from gui.widgets.graph_widget import GraphWidget
from gui.widgets.results_widget import ResultsWidget
from app.state.application_state import ApplicationState
from app.controllers.project_controller import ProjectController


class MainWindow(QMainWindow):
    """Main application window for PKinetix."""

    def __init__(self) -> None:
        super().__init__()
        self.application_state = ApplicationState()

        self.project_controller = ProjectController(
            self.application_state.project
        )
        self.analysis_engine = AnalysisEngine(
            self.application_state.project
        )
        self.project_controller.project_changed.connect(
             self._project_changed
        )



        self.setWindowTitle("PKinetix")
        self.resize(1400, 900)

        self._create_central_widget()
        self._create_layout()

        self.statusBar().showMessage("Ready")

    def _create_central_widget(self) -> None:
        """Create the application's central widget."""

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

    def _create_layout(self) -> None:
        """Create the main splitter layout."""

        # Create widgets
        self.study_information = StudyInformationWidget()
        self.graph = GraphWidget()
        self.results = ResultsWidget()
        self.data_table = DataTableWidget()
        self.data_table.data_changed.connect(
            self._on_data_changed
        )

        # Wrap widgets in panels
        study_panel = self._create_panel(
            "Study Information",
            self.study_information
        )

        graph_panel = self._create_panel(
            "Concentration-Time Plot",
            self.graph
        )

        results_panel = self._create_panel(
            "Results",
            self.results
        )

        table_panel = self._create_panel(
            "Concentration-Time Data",
            self.data_table
        )
        

        # Horizontal splitter
        top_splitter = QSplitter(Qt.Horizontal)

        top_splitter.addWidget(study_panel)
        top_splitter.addWidget(graph_panel)
        top_splitter.addWidget(results_panel)

        # Initial proportions
        top_splitter.setStretchFactor(0, 2)
        top_splitter.setStretchFactor(1, 6)
        top_splitter.setStretchFactor(2, 2)

        # Vertical splitter
        main_splitter = QSplitter(Qt.Vertical)

        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(table_panel)

        main_splitter.setStretchFactor(0, 65)
        main_splitter.setStretchFactor(1, 35)

        self.main_layout.addWidget(main_splitter)
        # Minimum sizes
        study_panel.setMinimumWidth(260)
        graph_panel.setMinimumWidth(450)
        results_panel.setMinimumWidth(240)


    def _create_panel(self, title: str, widget: QWidget) -> QGroupBox:

        """
        Create a titled panel that wraps a widget.
        """

        panel = QGroupBox(title)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 12, 8, 8)

        layout.addWidget(widget)

        return panel
    
    def _on_data_changed(self) -> None:
        """
        Update project model when table changes.
        """

        data = self.data_table.get_data()

        self.project_controller.update_observations(data)

        self.statusBar().showMessage(
            "Data updated"
        )
        
    def _project_changed(self) -> None:
        """
        Handle updates after the project model changes.
        """

        time, concentration = (
            self.analysis_engine.get_plot_data()
        )

        results = (
            self.project_controller.analysis_result
        )

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
                fitted_time=(
                    results.fitted_terminal_times
                ),
                fitted_concentration=(
                    results.fitted_terminal_concentrations
                ),
                highlighted_time=(
                    results.terminal_times
                ),
                highlighted_concentration=(
                    results.terminal_concentrations
                ),
            )

            self.results.update_results(
                results
            )

        self.statusBar().showMessage(
            f"{len(time)} observations loaded"
        )