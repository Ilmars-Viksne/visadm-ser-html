
"""
Core service orchestrating data ingestion, image embedding, and template rendering.
"""
from __future__ import annotations
import logging
from typing import Callable, List, Dict

from .models import RenderedDocument
from .exceptions import RenderError

logger = logging.getLogger(__name__)

FilenameStrategy = Callable[[Dict[str, str], int], str]


class MergeService:
    """Generates multiple HTML documents from records and a template engine.

    This service is UI-agnostic and returns a list of data transfer objects (DTOs)
    that any interface (CLI/GUI/API) can write to disk or serve to a client.

    Args:
        records: List of data rows (string dicts).
        template_engine: An object exposing `render(context: Dict[str, str]) -> str`.
        image_encoder: An object exposing `to_data_uri(path: str) -> Optional[str]`.
        image_path_field: Column name containing the image path (default: 'image_path').
        image_alt_field: Column name containing the image alt text (default: 'image_alt').
        filename_strategy: Function producing output filename from (row, index).
                           If not provided, a default strategy is used.

    Attributes:
        records: Cached list of row dictionaries.
        template_engine: The injected template engine.
        image_encoder: The injected image encoder.
        image_path_field: Name of the image path column.
        image_alt_field: Name of the image alt column.
        filename_strategy: Strategy function to determine output filenames.
    """

    def __init__(
        self,
        *,
        records: List[Dict[str, str]],
        template_engine,
        image_encoder,
        image_path_field: str = 'image_path',
        image_alt_field: str = 'image_alt',
        filename_strategy: FilenameStrategy = None
    ) -> None:
        self.records = records
        self.template_engine = template_engine
        self.image_encoder = image_encoder
        self.image_path_field = image_path_field
        self.image_alt_field = image_alt_field
        self.filename_strategy = filename_strategy or self._default_filename

    def _default_filename(self, row: Dict[str, str], idx: int) -> str:
        """Default filename strategy: `exam_variant_<variant>.html`.

        If the `variant` field is missing or empty, falls back to the row index.

        Args:
            row: The current data row.
            idx: Zero-based row index.

        Returns:
            A sanitized filename string.
        """
        variant = (row.get('variant') or '').strip()
        base = variant or str(idx + 1)
        safe = ''.join(c if c.isalnum() or c in ['_', '-', '.'] else '_' for c in f"exam_variant_{base}.html")
        return safe

    def generate(self) -> List[RenderedDocument]:
        """Generate HTML documents for all records.

        For each record, this:
          - Normalizes the context (stringifies None).
          - Computes a Base64 data URI from `image_path` (if present) and injects `image_src`.
          - Injects `image_alt` (if present).
          - Renders HTML via the template engine.
          - Builds a `RenderedDocument` with the computed filename.

        Returns:
            List[RenderedDocument]: All rendered documents.

        Raises:
            RenderError: If any unrecoverable error occurs during generation.
        """
        try:
            docs: List[RenderedDocument] = []
            for idx, row in enumerate(self.records):
                # Normalize context values
                ctx = {k: (v if isinstance(v, str) else ('' if v is None else str(v))) for k, v in row.items()}

                # Image handling
                img_path = (ctx.get(self.image_path_field) or '').strip()
                img_alt = (ctx.get(self.image_alt_field) or '').strip()
                img_src = self.image_encoder.to_data_uri(img_path) if img_path else None
                if img_src:
                    ctx['image_src'] = img_src
                if img_alt:
                    ctx['image_alt'] = img_alt

                # Render and collect
                html = self.template_engine.render(ctx)
                fname = self.filename_strategy(row, idx)
                docs.append(RenderedDocument(filename=fname, html=html))

            logger.info("Generated %d documents", len(docs))
            return docs

        except Exception as exc:
            # Convert any unexpected failure into a domain-specific error
            raise RenderError(f"Failed to generate documents: {exc}") from exc
