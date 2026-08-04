# JARVIS Web Calculator Suite

A modern, production-grade, responsive Web-based Calculator built with Flask, AST Math Evaluation, Unit Conversion, and persistent SQLite history tracking.

## Features

- **Standard & Scientific Calculator**: Full support for algebraic expressions, trigonometric functions (`sin`, `cos`, `tan`), logarithms, exponents, powers, factorials, and constants (`π`, `e`).
- **Safe Math Evaluation Engine**: Safe AST (Abstract Syntax Tree) parsing engine prevents code injection risks associated with Python's native `eval()`.
- **Unit Converter**: Multi-category conversion supporting Length, Mass/Weight, Temperature, Area, Volume, Speed, and Digital Storage units.
- **Calculation History**: Automatic real-time persistence of previous calculations in an SQLite database.
- **Interactive UI**: Supports dark & light mode toggles, DEG/RAD angle modes, full physical keyboard input support, memory controls (MC, MR, M+, M-, MS), and a mobile-friendly responsive design.

## Project Structure

```
calculator_app/
├── app.py                  # Main Flask Web Application & API endpoints
├── calculator/
│   ├── __init__.py
│   ├── engine.py           # AST-based Safe Math Parser & Scientific Evaluator
│   ├── converters.py       # Physical & Digital Unit Conversion Engine
│   └── history.py          # SQLite Calculation History Manager
├── templates/
│   └── index.html          # HTML5 UI Layout
├── static/
│   ├── css/
│   │   └── style.css       # Custom Glassmorphism UI Styles
│   └── js/
│       └── calculator.js    # Client-side Interactive Application Logic
├── requirements.txt        # Python Dependencies
└── README.md               # Documentation
```

## Quick Start & Installation

1. **Clone or Extract the Project Directory**:
   Ensure Python 3.8+ is installed on your system.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Website**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## Key Keyboard Shortcuts

- `0-9` : Number inputs
- `+`, `-`, `*`, `/`, `^` : Mathematical operators
- `Enter` or `=` : Evaluate calculation
- `Backspace` : Delete last character
- `Escape` : Clear display
- `(` and `)` : Parentheses for order of operations