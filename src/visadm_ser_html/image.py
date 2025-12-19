
"""
Image utilities (e.g., Base64 data URIs).
"""
from __future__ import annotations
import base64
from pathlib import Path
from mimetypes import guess_type
from typing import Optional

class DataUriEncoder:
    """Converts image files into Base64 data URIs."""

    def __init__(self, base_dir: str) -> None:
        """Initialize encoder with a base directory for relative paths.

        Args:
            base_dir: Directory against which relative image paths are resolved.
        """
        self.base_dir = Path(base_dir)

    def to_data_uri(self, src_path_str: str) -> Optional[str]:
        """Convert a path to a Base64 data URI.

        Args:
            src_path_str: Image path (absolute or relative to base_dir).

        Returns:
            A data URI string or None if the file does not exist.
        """
        if not src_path_str:
            return None
        # Normalize Windows separators
        src_path_str = src_path_str.replace('\\\\\\\\', '/').replace('\\\\', '/')
        p = Path(src_path_str)
        src_path = p if p.is_absolute() else (self.base_dir / p)
        if not src_path.exists():
            return None
        mime, _ = guess_type(src_path.name)
        if mime is None:
            mime = 'application/octet-stream'
        b = src_path.read_bytes()
        b64 = base64.b64encode(b).decode('ascii')
        return f"data:{mime};base64,{b64}"
