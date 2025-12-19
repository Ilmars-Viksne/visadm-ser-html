
# VisAdm Serial HTML

A modular Python package that generates serial, standalone HTML pages (Mail-merge style) using **Jinja2** templating, **Base64** image embedding, and **MathJax** rendering.

It cleanly separates **core business logic** (in `src/`) from the **presentation layer** (CLI/GUI), making it production-ready and testable.

---

## ✨ Key Features

- **Separation of Concerns**: Logic is decoupled from the file system and UI.
- **Standalone Outputs**: Images are embedded as **Base64** strings; no external assets required for the generated HTML.
- **MathJax Support**: Renders LaTeX-like formulas (e.g., `\frac`, `\sin`) in the browser.
- **Robustness**: Includes custom exceptions, logging, and type hinting.

---

## 📁 Project Structure

```text
.
├── src/
│   └── visadm_ser_html/    # Core package
│       ├── __init__.py
│       ├── config.py       # Env-var configuration
│       ├── data_source.py  # CSV/Excel reading
│       ├── exceptions.py   # Custom errors
│       ├── image.py        # Base64 encoding
│       ├── logging_config.py
│       ├── models.py       # DTOs
│       ├── service.py      # Main orchestration logic
│       └── template_engine.py
├── templates/
│   └── template.html       # Jinja2 HTML template
├── data/
│   └── data.csv            # Input data
├── config/
│   └── .env                # Environment variables
├── output/                 # Generated results
├── tests/
│   └── test_service.py
├── main.py                 # Entry point script
├── pyproject.toml          # Dependency management
└── README.md
```

---

## 🚀 Setup & Usage

### 1. Install Dependencies
It is recommended to use a virtual environment.

```bash
# Create and activate venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install the package in editable mode (crucial for src/ layout)
pip install -e .
```

### 2. Configure
Create a `.env` file in `config/` (or use the one provided):

```ini
VISADM_SER_HTML_DATA_PATH=data/data.csv
VISADM_SER_HTML_TEMPLATE_PATH=templates/template.html
VISADM_SER_HTML_OUTPUT_DIR=output
VISADM_SER_HTML_LOG_LEVEL=INFO
```

### 3. Run
```bash
python main.py
```

Check the `output/` directory for your generated HTML files.

---

## 🧪 Testing

Run the test suite using `pytest`:

```bash
pip install pytest
pytest
```

---

## 🔧 Troubleshooting

**Error: `ModuleNotFoundError: No module named 'visadm_ser_html'`**
*   **Cause:** Python cannot find the package in the `src` directory.
*   **Fix:** Ensure you ran `pip install -e .`.
*   **Alternative:** Run with `PYTHONPATH=src python main.py`.

**Images not appearing?**
*   Ensure the paths in `data.csv` are relative to the `data/` folder (or absolute).
*   Ensure the template uses `{{ image_src }}` inside an `<img>` tag.
