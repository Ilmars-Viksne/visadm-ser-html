
"""
Custom exceptions for the Exam Merge domain.
"""
from typing import Optional


class ExamMergeError(Exception):
    """Base exception for all domain-specific errors in Exam Merge."""


class DataSourceError(ExamMergeError):
    """Raised when there is a problem reading or parsing the data source (CSV/Excel/etc.)."""
    def __init__(self, message: str, *, path: Optional[str] = None) -> None:
        super().__init__(message)
        self.path = path


class TemplateError(ExamMergeError):
    """Raised when there is a problem compiling or rendering the template."""


class RenderError(ExamMergeError):
    """Raised when there is a problem producing rendered documents."""
