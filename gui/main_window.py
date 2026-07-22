from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.controllers.project_controller import ProjectController
from app.state.application_state import ApplicationState
from gui.widgets.data_table import DataTableWidget
from gui.widgets.graph_widget import GraphWidget
from gui.widgets.results_widget import (
    GoodnessOfFitWidget,
    ResultsWidget,
)
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

        self.setWindowTitle("PKinetix lite")
        self.resize(1500, 900)

        self._create_central_widget()
        self._create_layout()
        self._connect_signals()
        self._apply_theme()

        self.statusBar().showMessage("Ready")

    def _create_central_widget(self) -> None:
        """
        Create the central application widget.
        """

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(
            self.central_widget
        )
        self.main_layout.setContentsMargins(
            7,
            7,
            7,
            7,
        )
        self.main_layout.setSpacing(7)

    def _create_layout(self) -> None:
        """
        Create the complete application layout.
        """

        self.main_layout.addWidget(
            self._create_brand_header()
        )

        self.study_information = (
            StudyInformationWidget()
        )
        self.data_table = DataTableWidget()
        self.graph = GraphWidget()
        self.results = ResultsWidget()
        self.goodness_of_fit = (
            GoodnessOfFitWidget()
        )

        input_widget = self._create_input_widget()
        center_widget = self._create_center_widget()

        input_widget.setMinimumWidth(390)
        center_widget.setMinimumWidth(560)
        self.results.setMinimumWidth(350)

        self.workspace_splitter = QSplitter(
            Qt.Horizontal
        )

        self.workspace_splitter.addWidget(
            input_widget
        )
        self.workspace_splitter.addWidget(
            center_widget
        )
        self.workspace_splitter.addWidget(
            self.results
        )

        self.workspace_splitter.setStretchFactor(
            0,
            3,
        )
        self.workspace_splitter.setStretchFactor(
            1,
            5,
        )
        self.workspace_splitter.setStretchFactor(
            2,
            3,
        )

        self.workspace_splitter.setChildrenCollapsible(
            False
        )
        self.workspace_splitter.setSizes([
            430,
            700,
            370,
        ])
        self.workspace_splitter.setHandleWidth(7)

        self.main_layout.addWidget(
            self.workspace_splitter,
            1,
        )

    def _create_input_widget(self) -> QWidget:
        """
        Create the left input area.
        """

        widget = QWidget()

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        input_heading = QLabel("INPUT")
        input_heading.setObjectName(
            "majorHeading"
        )
        input_heading.setAlignment(Qt.AlignCenter)
        input_heading.setFixedHeight(36)

        layout.addWidget(input_heading)

        study_scroll = QScrollArea()
        study_scroll.setWidgetResizable(True)
        study_scroll.setFrameShape(
            QScrollArea.NoFrame
        )
        study_scroll.setWidget(
            self.study_information
        )

        table_container = QWidget()

        table_layout = QVBoxLayout(
            table_container
        )
        table_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        table_layout.setSpacing(5)

        table_heading = QLabel(
            "CONCENTRATION-TIME DATA"
        )
        table_heading.setObjectName(
            "sectionHeading"
        )
        table_heading.setAlignment(
            Qt.AlignCenter
        )
        table_heading.setFixedHeight(36)

        table_layout.addWidget(table_heading)
        table_layout.addWidget(
            self.data_table,
            1,
        )

        self.input_splitter = QSplitter(
            Qt.Vertical
        )
        self.input_splitter.addWidget(
            study_scroll
        )
        self.input_splitter.addWidget(
            table_container
        )

        self.input_splitter.setStretchFactor(
            0,
            4,
        )
        self.input_splitter.setStretchFactor(
            1,
            5,
        )
        self.input_splitter.setChildrenCollapsible(
            False
        )
        self.input_splitter.setSizes([
            360,
            440,
        ])
        self.input_splitter.setHandleWidth(7)

        layout.addWidget(
            self.input_splitter,
            1,
        )

        return widget

    def _create_center_widget(self) -> QWidget:
        """
        Create the graph and fit-statistics area.
        """

        widget = QWidget()

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        graph_container = QWidget()

        graph_layout = QVBoxLayout(
            graph_container
        )
        graph_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        graph_layout.setSpacing(5)

        graph_heading = QLabel(
            "CONCENTRATION-TIME PROFILE"
        )
        graph_heading.setObjectName(
            "majorHeading"
        )
        graph_heading.setAlignment(
            Qt.AlignCenter
        )
        graph_heading.setFixedHeight(36)

        graph_layout.addWidget(graph_heading)
        graph_layout.addWidget(
            self.graph,
            1,
        )

        self.center_splitter = QSplitter(
            Qt.Vertical
        )
        self.center_splitter.addWidget(
            graph_container
        )
        self.center_splitter.addWidget(
            self.goodness_of_fit
        )

        self.center_splitter.setStretchFactor(
            0,
            7,
        )
        self.center_splitter.setStretchFactor(
            1,
            3,
        )
        self.center_splitter.setChildrenCollapsible(
            False
        )
        self.center_splitter.setSizes([
            610,
            230,
        ])
        self.center_splitter.setHandleWidth(7)

        layout.addWidget(
            self.center_splitter,
            1,
        )

        return widget

    def _create_brand_header(self) -> QFrame:
        """
        Create the logo, name and copyright header.
        """

        frame = QFrame()
        frame.setObjectName("brandHeader")
        frame.setFixedHeight(58)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(
            12,
            5,
            14,
            5,
        )
        layout.setSpacing(10)

        logo_label = QLabel()
        logo_label.setObjectName("logoLabel")
        logo_label.setFixedSize(42, 42)
        logo_label.setAlignment(Qt.AlignCenter)

        project_root = (
            Path(__file__).resolve().parent.parent
        )

        logo_candidates = [
            project_root
            / "assets/logo/pkinetix_logo.png",
            project_root
            / "assets/logo/pkinetix_logo.jpg",
            project_root
            / "assets/logo/logo.png",
            project_root
            / "assets/logo/logo.jpg",
        ]

        for logo_path in logo_candidates:
            if not logo_path.exists():
                continue

            pixmap = QPixmap(str(logo_path))

            if pixmap.isNull():
                continue

            logo_label.setPixmap(
                pixmap.scaled(
                    38,
                    38,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )
            break

        software_name = QLabel(
            "PKinetix lite"
        )
        software_name.setObjectName(
            "softwareName"
        )
        software_name.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )

        copyright_label = QLabel(
            "© Nadeem Irfan Bukhari  |  "
            "Email: nadeem_irfan@hotmail.com"
        )
        copyright_label.setObjectName(
            "copyrightLabel"
        )
        copyright_label.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        layout.addWidget(logo_label)
        layout.addWidget(software_name)
        layout.addStretch()
        layout.addWidget(copyright_label)

        return frame

    def _connect_signals(self) -> None:
        """
        Connect GUI signals to controllers.
        """

        self.data_table.data_changed.connect(
            self._on_data_changed
        )

        self.study_information.data_changed.connect(
            self._on_study_information_changed
        )

        self.study_information.time_unit_changed.connect(
            self.data_table.convert_time_unit
        )

        self.study_information.concentration_unit_changed.connect(
            self.data_table.convert_concentration_unit
        )

        self.project_controller.project_changed.connect(
            self._project_changed
        )

    def _on_data_changed(self) -> None:
        """
        Update observations when table data changes.
        """

        self.project_controller.update_observations(
            self.data_table.get_data()
        )

    def _on_study_information_changed(
        self,
    ) -> None:
        """
        Update project information.
        """

        self.project_controller.update_study_information(
            self.study_information.get_data()
        )

    def _project_changed(self) -> None:
        """
        Refresh the graph and result displays.
        """

        time, concentration = (
            self.analysis_engine.get_plot_data()
        )

        results = (
            self.project_controller.analysis_result
        )

        self.results.update_units(
            self.application_state.project.units
        )

        if results is None:
            self.graph.plot_profile(
                time,
                concentration,
            )
            self.results.clear_results()
            self.goodness_of_fit.clear_results()
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

            self.results.update_results(results)

            self.goodness_of_fit.update_results(
                results
            )

        self.statusBar().showMessage(
            f"{len(time)} observations loaded"
        )

    def _apply_theme(self) -> None:
        """
        Apply the PKinetix teal and purple theme.
        """

        self.setStyleSheet("""
            /*
            MAIN COLORS

            Main window:
            #a9c8cc

            General panels:
            #b8d2d5

            Teal header:
            #91bdc3

            Purple headings:
            #b991bc

            Teal borders:
            #78adb3

            Dark text:
            #203f46
            */

            QMainWindow {
                background-color: #a9c8cc;
            }

            QWidget {
                background-color: #b8d2d5;
                color: #203f46;
                font-size: 13px;
            }

            #brandHeader {
                background-color: #91bdc3;
                border: 1px solid #63aeb7;
                border-radius: 5px;
            }

            #logoLabel {
                background-color: transparent;
            }

            #softwareName {
                color: #214f58;
                font-size: 22px;
                font-weight: 700;
                background-color: transparent;
            }

            #copyrightLabel {
                color: #345f66;
                background-color: transparent;
                font-size: 12px;
            }

            #majorHeading,
            #sectionHeading {
                background-color: #b991bc;
                border: 1px solid #956b9c;
                color: #392d3c;
                font-weight: 700;
                letter-spacing: 1px;
                border-radius: 3px;
                min-height: 36px;
                max-height: 36px;
            }

            QLineEdit,
            QTextEdit,
            QComboBox {
                background-color: rgba(
                    240,
                    249,
                    250,
                    180
                );
                color: #25454b;
                border: 1px solid #78adb3;
                border-radius: 3px;
                padding: 5px;
            }

            QLineEdit:hover,
            QTextEdit:hover,
            QComboBox:hover {
                background-color: rgba(
                    247,
                    252,
                    252,
                    210
                );
            }

            QLineEdit:focus,
            QTextEdit:focus,
            QComboBox:focus {
                background-color: #f5fbfc;
                border: 1px solid #438f99;
            }

            QComboBox QAbstractItemView {
                background-color: #e4f1f2;
                color: #25454b;
                border: 1px solid #6da6ad;
                outline: 0;
                padding: 4px;
            }

            QComboBox QAbstractItemView::item {
                min-height: 28px;
                padding: 5px 10px;
                border: none;
            }

            QComboBox QAbstractItemView::item:hover {
                background-color: #b7dadd;
                color: #183940;
            }

            QComboBox QAbstractItemView::item:selected {
                background-color: #78b4bb;
                color: #16363c;
                border: none;
            }

            #fixedUnitLabel {
                color: #315d64;
                padding-left: 5px;
                padding-right: 7px;
                font-weight: 600;
            }

            QTableWidget {
                background-color: rgba(
                    236,
                    247,
                    248,
                    200
                );
                color: #23454b;
                border: 1px solid #78adb3;
                gridline-color: transparent;
                selection-background-color: #85bcc2;
                selection-color: #16363c;
            }

            QTableWidget::item {
                background-color: transparent;
                border: none;
                border-bottom: 1px solid #91bdc2;
                padding: 5px;
            }

            QTableWidget::item:selected {
                background-color: #85bcc2;
                color: #16363c;
            }

            QHeaderView::section {
                background-color: #9fc9cd;
                color: #244a51;
                border: none;
                border-right: 1px solid #78adb3;
                border-bottom: 1px solid #78adb3;
                padding: 6px;
                font-weight: 700;
            }

            #plainResultValue {
                color: #215760;
                font-weight: 700;
                padding-right: 2px;
            }

            #resultUnit {
                color: #4c7279;
                font-size: 12px;
                padding-left: 4px;
            }

            #resultSeparator {
                background-color: #78aeb4;
                border: none;
            }

            QSplitter::handle {
                background-color: #72adb5;
            }

            QSplitter::handle:hover {
                background-color: #5297a0;
            }

            QScrollArea {
                border: none;
                background-color: transparent;
            }

            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }

            QScrollBar:vertical,
            QScrollBar:horizontal {
                background-color: #a8c9cc;
                border: none;
            }

            QScrollBar::handle {
                background-color: #76aeb5;
                border-radius: 3px;
                min-width: 20px;
                min-height: 20px;
            }

            QScrollBar::handle:hover {
                background-color: #5798a1;
            }

            QScrollBar::add-line,
            QScrollBar::sub-line {
                width: 0;
                height: 0;
            }

            QStatusBar {
                background-color: #91bdc3;
                color: #264f56;
                border-top: 1px solid #68a5ad;
            }

            QLabel {
                background-color: transparent;
            }
        """)