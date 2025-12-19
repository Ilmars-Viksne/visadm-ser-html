
"""
Domain models and data transfer objects.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class RenderedDocument:
    """A rendered HTML document.

    Attributes:
        filename: Suggested filename for the document (without path).
        html: Full HTML content.
    """
    filename: str
    html: str


@dataclass
class AppConfig:
    """Application configuration, decoupled from any UI.

    Attributes:
        data_path: Path to the input data file (CSV/Excel).
        template_path: Path to the HTML template file.
        output_dir: Directory where an interface should write rendered files.
        delimiter: CSV delimiter if using CSV.
        image_path_field: Column name for image path in the data.
        image_alt_field: Column name for image alt text.
        filename_field: Column name to drive filename generation (e.g., variant).
        log_level: Logging level (INFO/DEBUG/WARNING/etc.).
    """
    data_path: str
    template_path: str
    output_dir: str
    delimiter: str = ';'
    image_path_field: str = 'image_path'
    image_alt_field: str = 'image_alt'
    filename_field: str = 'variant'
    log_level: str = 'INFO'


# Simple type aliases for clarity in service/data layers
TemplateContext = Dict[str, str]
RowDict = Dict[str, str]
RowList = List[RowDict]
