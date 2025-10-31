from typing import Any, Callable, Dict, Optional, Union
import warnings

class ValidationResult:
    """Container for validation results."""

    def __init__(self, is_valid: bool, data: Any, errors: Optional[list]=None, warnings: Optional[list]=None):
        self.is_valid = is_valid
        self.data = data
        self.errors = errors or []
        self.warnings = warnings or []

    def add_warning(self, message: str):
        """Add a validation warning."""
        self.warnings.append(message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {'is_valid': self.is_valid, 'data': self.data, 'errors': self.errors, 'warnings': self.warnings}