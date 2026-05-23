
"""
Data source readers for CSV/JSON.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Protocol

import pandas as pd

from .exceptions import DataSourceError

logger = logging.getLogger(__name__)


class DataSource(Protocol):
    """Common interface for all data sources."""

    def read_rows(self) -> List[Dict[str, str]]:
        """Read rows as a list of dictionaries."""
        ...


def _value_to_string(value: Any) -> str:
    """Convert input value to a string suitable for Jinja templates."""
    if value is None:
        return ""

    # pandas may represent empty CSV cells as NaN
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass

    # For JSON lists/dicts, preserve structure as JSON text
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)

    return str(value)


def _normalize_row(row: Dict[str, Any]) -> Dict[str, str]:
    """Normalize all row values to strings."""
    return {str(key): _value_to_string(value) for key, value in row.items()}


class CSVDataSource:
    """Reads tabular data from a CSV file into a list of dictionaries.

    The class does not perform any user I/O and can be used by CLI or GUI layers.
    """

    def __init__(self, path: str, delimiter: str = ";") -> None:
        """Initialize the CSV data source.

        Args:
            path: Path to the CSV file.
            delimiter: Field delimiter used in the CSV.
        """
        self.path = Path(path)
        self.delimiter = delimiter

    def read_rows(self) -> List[Dict[str, str]]:
        """Read rows from the CSV as a list of dicts of strings.

        Returns:
            List[Dict[str, str]]: Row dictionaries.

        Raises:
            DataSourceError: If the file cannot be read.
        """
        try:
            df = pd.read_csv(self.path, sep=self.delimiter, dtype=str)
        except Exception as exc:
            raise DataSourceError(
                f"Failed to read CSV: {exc}",
                path=str(self.path),
            ) from exc

        rows: List[Dict[str, str]] = [
            _normalize_row(row.to_dict()) for _, row in df.iterrows()
        ]

        logger.debug("Read %d rows from %s", len(rows), self.path)
        return rows


class JSONDataSource:
    """Reads data from a JSON file into a list of dictionaries.

    Expected JSON structure:

    [
        {
            "filename": "doc_001.html",
            "title": "First document",
            "formula": "\\frac{F}{A}"
        },
        {
            "filename": "doc_002.html",
            "title": "Second document",
            "formula": "\\sin(x)"
        }
    ]
    """

    def __init__(self, path: str) -> None:
        """Initialize the JSON data source.

        Args:
            path: Path to the JSON file.
        """
        self.path = Path(path)

    def read_rows(self) -> List[Dict[str, str]]:
        """Read rows from JSON as a list of dicts of strings.

        Returns:
            List[Dict[str, str]]: Row dictionaries.

        Raises:
            DataSourceError: If the file cannot be read or has invalid structure.
        """
        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception as exc:
            raise DataSourceError(
                f"Failed to read JSON: {exc}",
                path=str(self.path),
            ) from exc

        if not isinstance(data, list):
            raise DataSourceError(
                "JSON data must be a list of objects.",
                path=str(self.path),
            )

        rows: List[Dict[str, str]] = []

        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise DataSourceError(
                    f"JSON item at index {index} is not an object.",
                    path=str(self.path),
                )

            rows.append(_normalize_row(item))

        logger.debug("Read %d rows from %s", len(rows), self.path)
        return rows


def create_data_source(path: str, delimiter: str = ";") -> DataSource:
    """Create the correct data source reader based on file extension."""
    suffix = Path(path).suffix.lower()

    if suffix == ".csv":
        return CSVDataSource(path, delimiter=delimiter)

    if suffix == ".json":
        return JSONDataSource(path)

    raise DataSourceError(
        f"Unsupported data file format: {suffix}. Supported formats: .csv, .json",
        path=path,
    )
