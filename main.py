
import os
from pathlib import Path
import logging

# Optional: load .env variables if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from visadm_ser_html.logging_config import setup_logging
from visadm_ser_html.config import load_config
from visadm_ser_html.data_source import CSVDataSource
from visadm_ser_html.template_engine import JinjaTemplateEngine
from visadm_ser_html.image import DataUriEncoder
from visadm_ser_html.service import MergeService

def write_documents(output_dir: Path, docs) -> None:
    """Write rendered documents to disk.

    Args:
        output_dir: Destination folder.
        docs: Iterable of RenderedDocument objects.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    for d in docs:
        (output_dir / d.filename).write_text(d.html, encoding='utf-8')


def main() -> None:
    setup_logging('INFO')
    cfg = load_config()
    logging.getLogger(__name__).info("Using config: %s", cfg)

    data_source = CSVDataSource(cfg.data_path, delimiter=cfg.delimiter)
    rows = data_source.read_rows()

    template_text = Path(cfg.template_path).read_text(encoding='utf-8')
    engine = JinjaTemplateEngine(template_text)

    image_enc = DataUriEncoder(base_dir=str(Path(cfg.data_path).parent))

    service = MergeService(
        records=rows,
        template_engine=engine,
        image_encoder=image_enc,
        image_path_field=cfg.image_path_field,
        image_alt_field=cfg.image_alt_field,
    )

    docs = service.generate()
    write_documents(Path(cfg.output_dir), docs)
    logging.getLogger(__name__).info("Done. Wrote %d documents to %s", len(docs), cfg.output_dir)


if __name__ == '__main__':
    main()
