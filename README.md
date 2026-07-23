# PKinetix

A modern, cross-platform pharmacokinetic analysis application designed to provide an intuitive, accurate, and professional alternative to legacy PK software.

PKinetix is being developed with a strong emphasis on scientific correctness, modular software architecture, performance, and an intuitive user experience. The software targets researchers, pharmacologists, pharmaceutical companies, universities, and healthcare professionals performing Non-Compartmental Analysis (NCA).

---

## Features

### Current

- Modern desktop interface built with PySide6
- Cross-platform support (Windows & macOS)
- Interactive concentration-time data table
- Study information management
- Real-time plotting
- Modular MVC-inspired architecture
- Scientific data validation
- Project state management

### Planned

- Full Non-Compartmental Analysis (NCA)
- Automatic terminal phase detection
- Lambda-z regression analysis
- AUC calculations
- AUMC calculations
- MRT calculations
- Clearance (CL)
- Volume of Distribution (Vz)
- Half-life estimation
- CSV Import / Export
- Excel Import / Export
- Publication-quality graph export
- Project save/load
- Batch processing
- Multiple dosing support
- Extensive validation engine
- Automatic route inference where possible
- Comprehensive reporting

---

## Technology Stack

- Python 3.13+
- PySide6
- NumPy
- SciPy
- Pandas
- Matplotlib
- SQLite
- OpenPyXL

---

## Project Structure

```
PKinetix/
│
├── app/
│   ├── controllers/
│   ├── models/
│   ├── services/
│   └── state/
│
├── gui/
│   ├── widgets/
│   └── main_window.py
│
├── io/
├── tests/
├── docs/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/ColdCoffee426/PKinetix.git
```

Navigate into the project:

```bash
cd PKinetix
```

Create a virtual environment:

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

## Development Goals

PKinetix is designed around several core principles:

- Scientific accuracy
- Modern user experience
- Maintainable architecture
- Extensibility
- Cross-platform compatibility
- High-performance numerical computation
- Testable calculation engine

Every pharmacokinetic calculation is designed to be independently testable and validated.

---

## Roadmap

- [x] Initial project architecture
- [x] Modern GUI framework
- [x] Data table implementation
- [x] Graph widget
- [x] Results panel
- [x] Validation framework
- [ ] File management
- [ ] Complete plotting engine
- [ ] NCA calculation engine
- [ ] Regression engine
- [ ] Statistical validation
- [ ] Report generation
- [ ] Packaging for Windows
- [ ] Packaging for macOS

---

## Contributing

Contributions, bug reports, and feature requests are welcome.

If you would like to contribute, please fork the repository and submit a pull request.

---

## License

This project is currently under development.

A license will be added before the first public release.

---

## Author

**Muhammad Qasim Bukhari**

Electrical & Electronics Engineer