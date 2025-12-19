
"""
Configuration loader (environment-driven).
"""
import os
from typing import Optional

from .models import AppConfig

# New prefix (preferred) with backward-compatibility for the old one.
ENV_PREFIX = 'VISADM_SER_HTML_'
FALLBACK_PREFIX = 'EXAMMERGE_'


def load_config() -> AppConfig:
    """Load application configuration from environment variables.

    Recognized variables (prefixed by ``VISADM_SER_HTML_``):
        DATA_PATH, TEMPLATE_PATH, OUTPUT_DIR, DELIMITER,
        IMAGE_PATH_FIELD, IMAGE_ALT_FIELD, FILENAME_FIELD, LOG_LEVEL.

    The loader also supports the legacy ``EXAMMERGE_`` prefix as a fallback,
    so existing environments remain compatible.

    Returns:
        AppConfig: Application configuration DTO.
    """
    def get(name: str, default: Optional[str] = None) -> str:
        return os.environ.get(
            ENV_PREFIX + name,
            os.environ.get(FALLBACK_PREFIX + name, default or '')
        )

    cfg = AppConfig(
        data_path=get('DATA_PATH', 'data/data.csv'),
        template_path=get('TEMPLATE_PATH', 'templates/template.html'),
        output_dir=get('OUTPUT_DIR', 'output'),
        delimiter=get('DELIMITER', ';'),
        image_path_field=get('IMAGE_PATH_FIELD', 'image_path'),
        image_alt_field=get('IMAGE_ALT_FIELD', 'image_alt'),
        filename_field=get('FILENAME_FIELD', 'variant'),
        log_level=get('LOG_LEVEL', 'INFO'),
    )
    return cfg
