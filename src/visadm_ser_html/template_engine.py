"""
Jinja2 template engine implementation.
"""
from typing import Dict, Any
from jinja2 import Environment, BaseLoader
from jinja2 import TemplateError as JinjaError

from .exceptions import TemplateError

class JinjaTemplateEngine:
    """A wrapper around Jinja2 to compile and render templates."""

    def __init__(self, template_text: str) -> None:
        """Initialize the engine with raw template text.

        Args:
            template_text: The HTML template string.

        Raises:
            TemplateError: If the template syntax is invalid.
        """
        try:
            # We use BaseLoader because we are passing the string directly,
            # not loading from a file system (Service layer handles file I/O).
            self.env = Environment(loader=BaseLoader(), autoescape=True)
            self.template = self.env.from_string(template_text)
        except Exception as exc:
            raise TemplateError(f"Failed to compile template: {exc}") from exc

    def render(self, context: Dict[str, Any]) -> str:
        """Render the template with the given context.

        Args:
            context: Dictionary of variables to inject.

        Returns:
            The rendered HTML string.

        Raises:
            TemplateError: If rendering fails.
        """
        try:
            return self.template.render(**context)
        except Exception as exc:
            raise TemplateError(f"Jinja2 rendering failed: {exc}") from exc