
import os
import re
import sys
from pathlib import Path

# Optional dependencies
try:
    import pandas as pd
except Exception as e:
    print("ERROR: pandas is required. Install with 'pip install pandas'.", file=sys.stderr)
    raise

try:
    from jinja2 import Environment
except Exception as e:
    print("ERROR: jinja2 is required. Install with 'pip install jinja2'.", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / 'templates'
DATA = ROOT / 'data'
OUTPUT = ROOT / 'output'

TEMPLATE_PATH = TEMPLATES / 'template.html'
DATA_PATH = DATA / 'data.csv'

OUTPUT.mkdir(parents=True, exist_ok=True)

def sanitize_filename(s: str) -> str:
    s = s.strip() or 'doc'
    return re.sub(r'[^0-9A-Za-z._-]+', '_', s)

def load_template_text(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    return text

def render_pages():
    # Read data
    df = pd.read_csv(DATA_PATH, sep=';', dtype=str)

    # Prepare template engine
    template_text = load_template_text(TEMPLATE_PATH)
    env = Environment(autoescape=True)
    template = env.from_string(template_text)

    count = 0
    for idx, row in df.iterrows():
        ctx = {k: (v if isinstance(v, str) else ('' if v is None else str(v))) for k, v in row.items()}
        variant = ctx.get('variant', '').strip()
        fname = sanitize_filename(f"exam_variant_{variant or idx+1}.html")
        html = template.render(**ctx)
        (OUTPUT / fname).write_text(html, encoding='utf-8')
        count += 1

    print(f"Generated {count} HTML file(s) in: {OUTPUT}")

if __name__ == '__main__':
    render_pages()
