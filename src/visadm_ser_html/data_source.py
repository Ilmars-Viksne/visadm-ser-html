
"""
Data source readers for CSV/Excel.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import List, Dict

import pandas as pd

from .exceptions import DataSourceError

logger = logging.getLogger(__name__)


class CSVDataSource:
    """Reads tabular data from a CSV file into a list of dictionaries.

    The class does not perform any user I/O and can be used by CLI or GUI layers.
    """

    def __init__(self, path: str, delimiter: str = ';') -> None:
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
            List[Dict[str, str]]: Row dictionaries (column name to string value).

        Raises:
            DataSourceError: If the file cannot be read.
        """
        try:
            df = pd.read_csv(self.path, sep=self.delimiter, dtype=str)
        except Exception as exc:
            raise DataSourceError(f"Failed to read CSV: {exc}", path=str(self.path)) from exc

        # Normalize None to empty strings
        rows: List[Dict[str, str]] = []
        for _, row in df.iterrows():
            rows.append({k: (v if isinstance(v, str) else ('' if v is None else str(v))) for k, v in row.items()})

        logger.debug("Read %d rows from %s", len(rows), self.path)
        return rows
