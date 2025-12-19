
from pathlib import Path

from src.visadm_ser_html.template_engine import JinjaTemplateEngine
from src.visadm_ser_html.image import DataUriEncoder
from src.visadm_ser_html.service import MergeService


def test_generate_documents(tmp_path: Path):
    template = (
        "<html><body>"
        "<p>Variant: {{ variant }}</p>"
        "{% if image_src %}<img src=\"{{ image_src }}\" />{% endif %}"
        "</body></html>"
    )
    engine = JinjaTemplateEngine(template)
    enc = DataUriEncoder(base_dir=str(tmp_path))

    # create a small file to encode
    img = tmp_path / 'pic.txt'
    img.write_text('hello', encoding='utf-8')

    rows = [
        {'variant': '1', 'image_path': 'pic.txt'},
        {'variant': '2', 'image_path': ''},
    ]
    svc = MergeService(records=rows, template_engine=engine, image_encoder=enc)
    docs = svc.generate()

    assert len(docs) == 2
    assert 'Variant: 1' in docs[0].html
    assert 'data:' in docs[0].html  # data URI present for first doc
    assert 'Variant: 2' in docs[1].html
