# OmniCalc - Advanced Web Calculator & Unit Converter

OmniCalc is a modern, high-performance web-based scientific calculator and multi-category unit converter built with Python Flask and vanilla JavaScript.

## Features

- **Standard & Scientific Calculator Modes**: Basic arithmetic, trigonometric functions, logarithms, roots, factorials, and mathematical constants ($\pi$, $e$).
- **Safe AST Math Engine**: Backend evaluation powered by Python's Abstract Syntax Tree (`ast`) parser, avoiding dangerous dynamic code execution while offering precise mathematical computation.
- **Unit Converter**: Converts units across Length, Mass, Temperature, and Digital Storage categories.
- **Calculation History**: Automatic tracking of calculations with clear/restore capabilities.
- **Keyboard Support**: Full physical keyboard support including shortcuts (`Enter` for calculate, `Backspace` for delete, `Escape` for clear).
- **Responsive & Modern Design**: Dark-mode primary UI with glassmorphism CSS, smooth animations, and optimized touch/click layouts for desktop and mobile.

## Project Structure

```
.
├── app.py                   # Flask server application and API endpoints
├── calculator/              # Core business logic module
│   ├── __init__.py
│   ├── converter.py         # Unit conversion algorithms
│   ├── evaluator.py         # Safe AST-based expression evaluator
│   └── history.py           # History storage manager
├── requirements.txt         # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css        # App styling and CSS variables
│   └── js/
│       └── calculator.js    # Client-side state, key bindings, and API bridge
└── templates/
    └── index.html           # Main Single Page Application HTML markup
```

## Setup & Running

### Prerequisites

- Python 3.9+ installed.

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to `http://127.0.0.1:5000`.

### Production Deployment

Run using `gunicorn`:
```bash
gunicorn app:app
```