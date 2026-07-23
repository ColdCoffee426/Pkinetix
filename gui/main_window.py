import csv
import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence, QTextDocument
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.controllers.project_controller import ProjectController
from app.state.application_state import ApplicationState
from gui.widgets.comparison_widget import ComparisonWidget
from gui.widgets.data_table import DataTableWidget
from gui.widgets.graph_widget import GraphWidget
from gui.widgets.results_widget import GoodnessOfFitWidget, ResultsWidget
from gui.widgets.study_information import StudyInformationWidget
from pk.analysis_engine import AnalysisEngine


class MainWindow(QMainWindow):
    """Main application window for the progressive PKinetix workflow."""

    HEADING_HEIGHT = 36

    def __init__(self) -> None:
        super().__init__()
        self.application_state = ApplicationState()
        self.project_controller = ProjectController(
            self.application_state.project
        )
        self.analysis_engine = AnalysisEngine(
            self.application_state.project
        )
        self.current_project_path: Path | None = None

        self.setWindowTitle("PKinetix Lite")
        self.resize(1400, 820)

        self._create_actions()
        self._create_menus()
        self._create_central_widget()
        self._create_layout()
        self._connect_signals()
        self._apply_theme()

        self.statusBar().showMessage("Enter study data, then choose Calculate → Analyze")

    def _create_actions(self) -> None:
        self.new_action = QAction("New Analysis", self)
        self.new_action.setShortcut(QKeySequence.New)
        self.new_action.triggered.connect(self._new_analysis)

        self.open_action = QAction("Open Project…", self)
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self._open_project)

        self.save_action = QAction("Save", self)
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self._save_project)

        self.save_as_action = QAction("Save As…", self)
        self.save_as_action.setShortcut(QKeySequence.SaveAs)
        self.save_as_action.triggered.connect(self._save_project_as)

        self.import_csv_action = QAction("Import CSV/Text…", self)
        self.import_csv_action.triggered.connect(self._import_data)

        self.export_pdf_action = QAction("Export Results as PDF…", self)
        self.export_pdf_action.triggered.connect(self._export_pdf)

        self.export_word_action = QAction("Export Results for Word…", self)
        self.export_word_action.triggered.connect(self._export_word)

        self.export_graph_action = QAction("Export Graph…", self)
        self.export_graph_action.triggered.connect(self._export_graph)

        self.quit_action = QAction("Quit", self)
        self.quit_action.setShortcut(QKeySequence.Quit)
        self.quit_action.triggered.connect(self.close)

        self.analyze_action = QAction("Analyze", self)
        self.analyze_action.setShortcut(Qt.Key_Return)
        self.analyze_action.triggered.connect(self._run_analysis)

        self.advanced_action = QAction("Advanced Analysis", self)
        self.advanced_action.triggered.connect(self._show_comparison_page)

        self.edit_data_action = QAction("Edit Entered Data", self)
        self.edit_data_action.triggered.connect(self._show_input_page)

        self.fullscreen_action = QAction("Full Screen", self)
        self.fullscreen_action.setShortcut("F11")
        self.fullscreen_action.triggered.connect(self._toggle_fullscreen)

        self.normal_size_action = QAction("Normal Window", self)
        self.normal_size_action.triggered.connect(self.showNormal)

        self.maximize_action = QAction("Maximize", self)
        self.maximize_action.triggered.connect(self.showMaximized)

        self.about_action = QAction("About PKinetix", self)
        self.about_action.triggered.connect(self._show_about)

    def _create_menus(self) -> None:
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.import_csv_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_pdf_action)
        file_menu.addAction(self.export_word_action)
        file_menu.addAction(self.export_graph_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        calculate_menu = self.menuBar().addMenu("Calculate")
        calculate_menu.addAction(self.analyze_action)
        calculate_menu.addAction(self.advanced_action)

        options_menu = self.menuBar().addMenu("Options")
        options_menu.addAction(self.edit_data_action)

        window_menu = self.menuBar().addMenu("Window")
        window_menu.addAction(self.fullscreen_action)
        window_menu.addAction(self.maximize_action)
        window_menu.addAction(self.normal_size_action)

        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_action)

    def _create_central_widget(self) -> None:
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(7, 7, 7, 7)
        self.main_layout.setSpacing(7)

    def _create_layout(self) -> None:
        self.main_layout.addWidget(self._create_brand_header())

        self.study_information = StudyInformationWidget()
        self.data_table = DataTableWidget()
        self.graph = GraphWidget()
        self.results = ResultsWidget()
        self.goodness_of_fit = GoodnessOfFitWidget()
        self.comparison = ComparisonWidget()
        self.analysis_data_table = QTableWidget(0, 2)
        self.analysis_data_table.setHorizontalHeaderLabels([
            "Time",
            "Concentration",
        ])
        self.analysis_data_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.analysis_data_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.pages = QStackedWidget()
        self.input_page = self._create_input_page()
        self.analysis_page = self._create_analysis_page()
        self.comparison_page = self._create_comparison_page()
        self.pages.addWidget(self.input_page)
        self.pages.addWidget(self.analysis_page)
        self.pages.addWidget(self.comparison_page)
        self.main_layout.addWidget(self.pages, 1)
        self.pages.setCurrentWidget(self.input_page)

    def _create_input_page(self) -> QWidget:
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(6)

        input_heading = self._heading("INPUT")
        page_layout.addWidget(input_heading)

        study_scroll = QScrollArea()
        study_scroll.setWidgetResizable(True)
        study_scroll.setFrameShape(QScrollArea.NoFrame)
        study_scroll.setWidget(self.study_information)

        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(5)
        table_layout.addWidget(self._heading("CONCENTRATION-TIME DATA"))
        table_layout.addWidget(self.data_table, 1)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(study_scroll)
        splitter.addWidget(table_container)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([480, 800])
        splitter.setHandleWidth(7)
        page_layout.addWidget(splitter, 1)

        button_row = QHBoxLayout()
        button_row.addStretch()
        calculate_button = QPushButton("Calculate")
        calculate_button.setObjectName("primaryButton")
        calculate_button.clicked.connect(self._run_analysis)
        button_row.addWidget(calculate_button)
        page_layout.addLayout(button_row)
        return page

    def _create_analysis_page(self) -> QWidget:
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(6)

        body_splitter = QSplitter(Qt.Horizontal)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self._heading("INPUT DATA"))
        left_layout.addWidget(self.analysis_data_table, 1)

        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        graph_container = QWidget()
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(0, 0, 0, 0)
        graph_layout.addWidget(self._heading("CONCENTRATION-TIME PROFILE"))
        graph_layout.addWidget(self.graph, 1)

        center_splitter = QSplitter(Qt.Vertical)
        center_splitter.addWidget(graph_container)
        center_splitter.addWidget(self.goodness_of_fit)
        center_splitter.setStretchFactor(0, 7)
        center_splitter.setStretchFactor(1, 3)
        center_splitter.setChildrenCollapsible(False)
        center_splitter.setSizes([590, 220])
        center_layout.addWidget(center_splitter)

        body_splitter.addWidget(left)
        body_splitter.addWidget(center)
        body_splitter.addWidget(self.results)
        body_splitter.setStretchFactor(0, 2)
        body_splitter.setStretchFactor(1, 5)
        body_splitter.setStretchFactor(2, 3)
        body_splitter.setChildrenCollapsible(False)
        body_splitter.setSizes([320, 700, 390])
        body_splitter.setHandleWidth(7)
        page_layout.addWidget(body_splitter, 1)

        navigation = QHBoxLayout()
        edit_button = QPushButton("Edit Data")
        edit_button.clicked.connect(self._show_input_page)
        next_button = QPushButton("Next: Comparison")
        next_button.setObjectName("primaryButton")
        next_button.clicked.connect(self._show_comparison_page)
        navigation.addWidget(edit_button)
        navigation.addStretch()
        navigation.addWidget(next_button)
        page_layout.addLayout(navigation)
        return page

    def _create_comparison_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.comparison, 1)
        navigation = QHBoxLayout()
        back_button = QPushButton("Back to Analysis")
        back_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.analysis_page)
        )
        navigation.addWidget(back_button)
        navigation.addStretch()
        layout.addLayout(navigation)
        return page

    def _create_brand_header(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("brandHeader")
        frame.setFixedHeight(40)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(14, 5, 14, 5)

        software_name = QLabel("PKinetix lite")
        software_name.setObjectName("softwareName")
        software_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        copyright_label = QLabel(
            "© Nadeem Irfan Bukhari  |  Email: nadeem_irfan@hotmail.com"
        )
        copyright_label.setObjectName("copyrightLabel")
        copyright_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(software_name)
        layout.addStretch()
        layout.addWidget(copyright_label)
        return frame

    def _heading(self, text: str) -> QLabel:
        heading = QLabel(text)
        heading.setObjectName("majorHeading")
        heading.setAlignment(Qt.AlignCenter)
        heading.setFixedHeight(self.HEADING_HEIGHT)
        return heading

    def _connect_signals(self) -> None:
        self.data_table.data_changed.connect(self._on_data_changed)
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
        self.project_controller.update_observations(
            self.data_table.get_data()
        )
        self.statusBar().showMessage(
            "Data updated. Choose Calculate → Analyze to calculate results."
        )

    def _on_study_information_changed(self) -> None:
        self.project_controller.update_study_information(
            self.study_information.get_data()
        )

    def _run_analysis(self) -> None:
        self._on_study_information_changed()
        self._on_data_changed()
        results = self.project_controller.analyze()

        if results is None:
            errors = []
            if self.project_controller.project_validation is not None:
                errors.extend(
                    self.project_controller.project_validation.errors
                )
            for validation in self.project_controller.validation_errors:
                errors.extend(validation.errors)

            QMessageBox.warning(
                self,
                "Unable to Analyze",
                "\n".join(errors) if errors else "Please check the entered data.",
            )
            return

        self._populate_analysis_table()
        self._update_analysis_display()
        self.pages.setCurrentWidget(self.analysis_page)
        self.statusBar().showMessage("Analysis completed")

    def _project_changed(self) -> None:
        self.results.update_units(self.application_state.project.units)

    def _update_analysis_display(self) -> None:
        time, concentration = self.analysis_engine.get_plot_data()
        results = self.project_controller.analysis_result
        if results is None:
            return

        self.graph.plot_profile(
            time,
            concentration,
            fitted_time=results.fitted_terminal_times,
            fitted_concentration=results.fitted_terminal_concentrations,
            highlighted_time=results.terminal_times,
            highlighted_concentration=results.terminal_concentrations,
        )
        self.results.update_results(results)
        self.goodness_of_fit.update_results(results)
        self.comparison.set_observations(list(zip(time, concentration)))

    def _populate_analysis_table(self) -> None:
        observations = self.application_state.project.observations
        self.analysis_data_table.setRowCount(len(observations))
        self.analysis_data_table.setHorizontalHeaderLabels([
            f"Time ({self.application_state.project.units.time})",
            f"Concentration ({self.application_state.project.units.concentration})",
        ])
        for row, observation in enumerate(observations):
            self.analysis_data_table.setItem(
                row,
                0,
                QTableWidgetItem(f"{observation.time:g}"),
            )
            self.analysis_data_table.setItem(
                row,
                1,
                QTableWidgetItem(f"{observation.concentration:g}"),
            )

    def _show_input_page(self) -> None:
        self.pages.setCurrentWidget(self.input_page)
        self.statusBar().showMessage("Editing project data")

    def _show_comparison_page(self) -> None:
        if self.project_controller.analysis_result is None:
            QMessageBox.information(
                self,
                "Analysis Required",
                "Run Calculate → Analyze before opening the comparison page.",
            )
            return
        self.pages.setCurrentWidget(self.comparison_page)

    def _new_analysis(self) -> None:
        self.application_state.project.observations.clear()
        self.study_information.set_data({})
        self.data_table.clear_data()
        self.project_controller.clear_analysis()
        self.graph.clear_plot()
        self.results.clear_results()
        self.goodness_of_fit.clear_results()
        self.current_project_path = None
        self.pages.setCurrentWidget(self.input_page)
        self.statusBar().showMessage("New analysis")

    def _project_payload(self) -> dict:
        project = self.application_state.project
        return {
            "study_name": project.study_name,
            "drug_name": project.drug_name,
            "subject_id": project.subject_id,
            "dose": project.dose,
            "body_weight": project.body_weight,
            "comments": project.comments,
            "route": project.route,
            "auc_method": project.auc_method,
            "units": {
                "time": project.units.time,
                "concentration": project.units.concentration,
                "dose": project.units.dose,
                "body_weight": project.units.body_weight,
            },
            "observations": [
                {
                    "time": observation.time,
                    "concentration": observation.concentration,
                }
                for observation in project.observations
            ],
        }

    def _save_project(self) -> None:
        if self.current_project_path is None:
            self._save_project_as()
            return
        self.current_project_path.write_text(
            json.dumps(self._project_payload(), indent=2),
            encoding="utf-8",
        )
        self.statusBar().showMessage(f"Saved {self.current_project_path.name}")

    def _save_project_as(self) -> None:
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save PKinetix Project",
            "",
            "PKinetix Project (*.pkinetix.json);;JSON (*.json)",
        )
        if not filename:
            return
        self.current_project_path = Path(filename)
        self._save_project()

    def _open_project(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open PKinetix Project",
            "",
            "PKinetix Project (*.pkinetix.json *.json)",
        )
        if not filename:
            return

        try:
            payload = json.loads(Path(filename).read_text(encoding="utf-8"))
            units = payload.get("units", {})
            self.study_information.set_data({
                **payload,
                "time_unit": units.get("time", "h"),
                "concentration_unit": units.get("concentration", "ng/mL"),
            })
            rows = [
                (float(row["time"]), float(row["concentration"]))
                for row in payload.get("observations", [])
            ]
            self.data_table.time_unit = units.get("time", "h")
            self.data_table.concentration_unit = units.get(
                "concentration",
                "ng/mL",
            )
            self.data_table.set_data(rows)
            self.current_project_path = Path(filename)
            self.pages.setCurrentWidget(self.input_page)
            self.statusBar().showMessage(f"Opened {Path(filename).name}")
        except (OSError, ValueError, KeyError, TypeError) as error:
            QMessageBox.critical(self, "Open Failed", str(error))

    def _import_data(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import Concentration-Time Data",
            "",
            "Data Files (*.csv *.txt);;All Files (*)",
        )
        if not filename:
            return

        rows = []
        try:
            with open(filename, newline="", encoding="utf-8-sig") as source:
                sample = source.read(2048)
                source.seek(0)
                dialect = csv.Sniffer().sniff(sample, delimiters=",\t; ")
                reader = csv.reader(source, dialect)
                for raw_row in reader:
                    if len(raw_row) < 2:
                        continue
                    try:
                        rows.append((float(raw_row[0]), float(raw_row[1])))
                    except ValueError:
                        continue
        except (OSError, csv.Error) as error:
            QMessageBox.critical(self, "Import Failed", str(error))
            return

        if not rows:
            QMessageBox.warning(self, "Import Failed", "No numeric rows were found.")
            return

        self.data_table.set_data(rows)
        self.statusBar().showMessage(f"Imported {len(rows)} observations")

    def _report_html(self) -> str:
        results = self.project_controller.analysis_result
        if results is None:
            raise ValueError("Run an analysis before exporting results.")

        project = self.application_state.project
        result_rows = []
        for attribute, label in self.results.labels.items():
            title = self.results.title_labels[attribute].text()
            result_rows.append(
                f"<tr><td>{title}</td><td>{label.text()}</td></tr>"
            )

        return f"""
        <html><body>
        <h1>PKinetix Lite Analysis Report</h1>
        <p><b>Study:</b> {project.study_name}</p>
        <p><b>Drug:</b> {project.drug_name}</p>
        <p><b>Subject ID:</b> {project.subject_id}</p>
        <p><b>Dose:</b> {project.dose or '--'} {project.units.dose}</p>
        <p><b>Route:</b> {project.route or '--'}</p>
        <h2>Pharmacokinetic Parameters</h2>
        <table border="1" cellspacing="0" cellpadding="5">
        {''.join(result_rows)}
        </table>
        <h2>Remarks</h2>
        <p>{project.comments or '--'}</p>
        </body></html>
        """

    def _export_pdf(self) -> None:
        try:
            html = self._report_html()
        except ValueError as error:
            QMessageBox.information(self, "Export", str(error))
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export PDF Report",
            "PKinetix_Report.pdf",
            "PDF (*.pdf)",
        )
        if not filename:
            return

        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(filename)
        document = QTextDocument()
        document.setHtml(html)
        document.print_(printer)
        self.statusBar().showMessage("PDF report exported")

    def _export_word(self) -> None:
        try:
            html = self._report_html()
        except ValueError as error:
            QMessageBox.information(self, "Export", str(error))
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Word-Compatible Report",
            "PKinetix_Report.doc",
            "Word-Compatible Document (*.doc)",
        )
        if not filename:
            return

        Path(filename).write_text(html, encoding="utf-8")
        self.statusBar().showMessage("Word-compatible report exported")

    def _export_graph(self) -> None:
        if self.project_controller.analysis_result is None:
            QMessageBox.information(self, "Export", "Run an analysis first.")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Graph",
            "PKinetix_Graph.png",
            "PNG (*.png);;JPEG (*.jpg);;TIFF (*.tiff);;SVG (*.svg);;PDF (*.pdf)",
        )
        if filename:
            self.graph.canvas.figure.savefig(filename, dpi=300, bbox_inches="tight")
            self.statusBar().showMessage("Graph exported")

    def _toggle_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About PKinetix",
            "PKinetix Lite\nProgressive pharmacokinetic analysis software.\n"
            "NCA is active; compartmental fitting is under development.",
        )

    def _apply_theme(self) -> None:
        self.setStyleSheet("""
            QMainWindow { background-color: #9fc7ef; }
            QWidget { background-color: #b8d7f4; color: #163a5c; font-size: 13px; }
            QMenuBar { background-color: #156dc6; color: white; padding: 3px; }
            QMenuBar::item:selected { background-color: #22baba; color: white; }
            QMenu { background-color: #eef6fd; color: #163a5c; border: 1px solid #6fa8df; }
            QMenu::item { padding: 7px 28px 7px 12px; }
            QMenu::item:selected { background-color: #156dc6; color: white; }
            #brandHeader { background-color: #156dc6; border: 1px solid #0f58a5; border-radius: 5px; }
            #softwareName { color: white; font-size: 22px; font-weight: 700; background-color: transparent; }
            #copyrightLabel { color: white; background-color: transparent; font-size: 12px; }
            #majorHeading, #sectionHeading { background-color: #22baba; border: 1px solid #168f8f; color: white; font-weight: 700; letter-spacing: 1px; border-radius: 3px; }
            QLineEdit, QTextEdit, QComboBox { background-color: #edf6fd; color: #163a5c; border: 1px solid #6fa8df; border-radius: 3px; padding: 5px; min-height: 22px; }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus { background-color: white; border: 1px solid #156dc6; }
            QComboBox::drop-down { border: none; width: 26px; }
            QComboBox QAbstractItemView { background-color: white; color: #163a5c; border: 1px solid #156dc6; outline: 0; padding: 4px; min-width: 280px; }
            QComboBox QAbstractItemView::item { min-height: 30px; padding: 6px 10px; border: none; }
            QComboBox QAbstractItemView::item:selected { background-color: #156dc6; color: white; }
            #fixedUnitLabel { color: #163a5c; padding-left: 5px; font-weight: 600; }
            QTableWidget { background-color: white; alternate-background-color: white; color: #163a5c; border: 1px solid #6fa8df; gridline-color: #8db9e5; selection-background-color: #156dc6; selection-color: white; }
            QTableWidget::item { background-color: white; padding: 5px; }
            QTableWidget::item:selected { background-color: #156dc6; color: white; }
            QTableWidget QLineEdit { background-color: white; color: #163a5c; border: 2px solid #156dc6; padding: 3px 5px; min-height: 28px; }
            QHeaderView::section { background-color: #d7e9f9; color: #163a5c; border: 1px solid #8db9e5; padding: 6px; font-weight: 700; }
            #plainResultValue { background-color: transparent; color: white; font-weight: 700; padding-right: 2px; }
            #resultSeparator { background-color: #6fa8df; border: none; }
            QSplitter::handle { background-color: #156dc6; }
            QSplitter::handle:hover { background-color: #0f5ba7; }
            QScrollArea { border: none; background-color: transparent; }
            QScrollArea > QWidget > QWidget { background-color: transparent; }
            QScrollBar:vertical, QScrollBar:horizontal { background-color: #d7e9f9; border: none; }
            QScrollBar::handle { background-color: #7f4f9f; border-radius: 4px; min-width: 22px; min-height: 22px; }
            QScrollBar::handle:hover { background-color: #633b80; }
            QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }
            QPushButton { background-color: #edf6fd; color: #163a5c; border: 1px solid #156dc6; border-radius: 4px; padding: 7px 18px; font-weight: 600; }
            QPushButton:hover { background-color: #d7e9f9; }
            #primaryButton { background-color: #156dc6; color: white; }
            #primaryButton:hover { background-color: #0f5ba7; }
            QStatusBar { background-color: #156dc6; color: white; border-top: 1px solid #0f58a5; }
            QLabel { background-color: transparent; }
        """)
