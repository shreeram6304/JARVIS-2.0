# Modern Scientific Calculator Web Application

A full-featured, responsive, production-ready web calculator built with Python (Flask) and modern vanilla JavaScript/CSS. Supports standard and scientific mathematical expressions, safe server-side evaluation via AST parsing, persistent SQLite calculation history, keyboard shortcuts, and theme customization.

## Features

- **Standard & Scientific Operations**: Trigonometry, logarithms, factorials, powers, roots, and standard arithmetic.
- **Safe Evaluation Engine**: Custom AST-based Python math engine ensuring secure expression evaluation without `eval()` vulnerabilities.
- **Persistent History**: SQLite database backing to record, retrieve, and clear calculation history.
- **Responsive UI**: Sleek glassmorphism visual design with support for Standard and Scientific view toggles, Light/Dark themes, and mobile layout adaptivity.
- **Keyboard Navigation**: Full keyboard shortcut support for rapid calculations.
- **RESTful API**: Clean API separation between business logic and UI presentation.

## Project Structure

```text
.
├── app.py                  # Flask application entry point
├── calculator/
│   ├── __init__.py         # Package initializer
│   ├── engine.py           # Safe AST-based mathematical evaluation engine
│   ├── history.py          # SQLite history storage service
│   └── routes.py           # Blueprint API endpoints
├── static/
│   ├── css/
│   │   └── style.css       # Responsive styling & dynamic themes
│   └── js/
│       └── app.js          # Client-side calculator controller & keyboard bindings
├── templates/
│   └── index.html          # Web interface template
└── requirements.txt        # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `pip` package manager

### Installation

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

3. Open your web browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

## Keyboard Shortcuts

- `0` - `9`, `.`: Input numbers and decimals
- `+`, `-`, `*`, `/`, `%`, `^`: Arithmetic operators
- `Enter` or `=`: Calculate result
- `Backspace`: Delete last character
- `Escape` or `c` / `C`: Clear input
- `(` / `)`: Parentheses for complex expressions