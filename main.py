
import os
import re
import sys
from pathlib import Path
import base64
from mimetypes import guess_type

# deps
try:
    import pandas as pd
except Exception:
    print("ERROR: pandas is required. Install with 'pip install pandas'.", file=sys.stderr)
    raise

try:
    from jinja2 import Environment
except Exception:
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
    return path.read_text(encoding='utf-8')

def to_data_uri(src_path_str: str, data_dir: Path) -> str | None:
    """
    Returns a data URI (data:<mime>;base64,...) for a local image.
    Paths in CSV are treated as relative to data_dir unless absolute.
    """
    if not src_path_str:
        return None
    p = Path(src_path_str)
    src_path = p if p.is_absolute() else (data_dir / p)
    if not src_path.exists():
        # You can log a warning here if desired
        return None
    mime, _ = guess_type(src_path.name)
    if mime is None:
        # reasonable fallback
        mime = 'application/octet-stream'
    b = src_path.read_bytes()
    b64 = base64.b64encode(b).decode('ascii')
    return f"data:{mime};base64,{b64}"

def render_pages():
    # Read data
    df = pd.read_csv(DATA_PATH, sep=';', dtype=str)

    # Prepare template engine
    template_text = load_template_text(TEMPLATE_PATH)
    env = Environment(autoescape=True)
    template = env.from_string(template_text)

    count = 0
    for idx, row in df.iterrows():
        # string-ify and clean None values
        ctx = {k: (v if isinstance(v, str) else ('' if v is None else str(v))) for k, v in row.items()}

        # Build base64 data URI from image_path
        image_path = (ctx.get('image_path') or '').strip()
        ctx['image_src'] = to_data_uri(image_path, DATA)
        ctx['image_alt'] = (ctx.get('image_alt') or '').strip()

        # Filename logic
        variant = ctx.get('variant', '').strip()
        fname = sanitize_filename(f"exam_variant_{variant or idx+1}.html")

        # Render and write
        html = template.render(**ctx)
        (OUTPUT / fname).write_text(html, encoding='utf-8')
        count += 1

    print(f"Generated {count} HTML file(s) in: {OUTPUT}")

if __name__ == '__main__':
    render_pages()
