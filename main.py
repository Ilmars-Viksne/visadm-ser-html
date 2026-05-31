import logging
from pathlib import Path

# Optional: load .env variables if present
try:
    from dotenv import load_dotenv
    load_dotenv(Path("config") / ".env")
except Exception:
    pass


from visadm_ser_html.logging_config import setup_logging
from visadm_ser_html.config import load_config
from visadm_ser_html.data_source import create_data_source
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
        (output_dir / d.filename).write_text(d.html, encoding="utf-8")


def add_embedded_image_sources(rows, image_encoder) -> None:
    """For every field ending with '_image_path', create a matching '_image_src' field.

    Example:
        SZ78_C5_image_path -> SZ78_C5_image_src
        beam_image_path    -> beam_image_src
        diagram_image_path -> diagram_image_src
    """
    for row in rows:
        image_path_keys = [
            key for key in row.keys()
            if key.endswith("_image_path")
        ]

        for path_key in image_path_keys:
            src_key = path_key.removesuffix("_image_path") + "_image_src"

            image_path = row.get(path_key, "")

            if image_path:
                row[src_key] = image_encoder.to_data_uri(image_path)
            else:
                row[src_key] = ""


def main() -> None:
    setup_logging("INFO")
    cfg = load_config()
    logging.getLogger(__name__).info("Using config: %s", cfg)

    data_source = create_data_source(cfg.data_path, delimiter=cfg.delimiter)
    rows = data_source.read_rows()

    image_enc = DataUriEncoder(base_dir=str(Path(cfg.data_path).parent))

    # Automatically embed all custom image fields ending with "_image_path"
    add_embedded_image_sources(rows, image_enc)

    template_text = Path(cfg.template_path).read_text(encoding="utf-8")
    engine = JinjaTemplateEngine(template_text)

    service = MergeService(
        records=rows,
        template_engine=engine,
        image_encoder=image_enc,
        image_path_field=cfg.image_path_field,
        image_alt_field=cfg.image_alt_field,
    )

    docs = service.generate()
    write_documents(Path(cfg.output_dir), docs)

    logging.getLogger(__name__).info(
        "Done. Wrote %d documents to %s",
        len(docs),
        cfg.output_dir,
    )


if __name__ == "__main__":
    main()