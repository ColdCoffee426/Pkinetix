from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSplitter,
)

from gui.widgets.study_information import StudyInformationWidget
from gui.widgets.data_table import DataTableWidget
from gui.widgets.graph_widget import GraphWidget
from gui.widgets.results_widget import ResultsWidget


class MainWindow(QMainWindow):
    """Main application window for PKinetix."""

    def __init__(self) -> None:
        super().__init__()

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

        # Horizontal splitter
        top_splitter = QSplitter(Qt.Horizontal)

        top_splitter.addWidget(self.study_information)
        top_splitter.addWidget(self.graph)
        top_splitter.addWidget(self.results)

        # Initial proportions
        top_splitter.setStretchFactor(0, 2)
        top_splitter.setStretchFactor(1, 5)
        top_splitter.setStretchFactor(2, 2)

        # Vertical splitter
        main_splitter = QSplitter(Qt.Vertical)

        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.data_table)

        main_splitter.setStretchFactor(0, 3)
        main_splitter.setStretchFactor(1, 2)

        self.main_layout.addWidget(main_splitter)