from fletx.utils.exceptions import TemplateError, ValidationError
import re
from pathlib import Path

class TemplateValidator:
    """
    Validates template names and ensures they follow conventions.
    """

    @staticmethod
    def validate_name(name: str, target_type: str='template') -> None:
        """
        Validate a template name.

        Args:
            name: The name to validate
            target_type: Type of template (for error messages)
        """
        if not name:
            raise ValidationError(f'{target_type.capitalize()} name cannot be empty.')
        if not re.match('^[a-zA-Z][a-zA-Z0-9_]*$', name):
            raise ValidationError(f'{target_type.capitalize()} name must start with a letter and contain only letters, numbers, and underscores.')
        if len(name) > 50:
            raise ValidationError(f'{target_type.capitalize()} name is too long (max 50 characters).')
        import keyword
        if keyword.iskeyword(name):
            raise ValidationError(f"'{name}' is a Python keyword and cannot be used as a {target_type} name.")
        common_modules = {'sys', 'os', 'json', 'time', 'datetime', 'random', 'math', 'collections', 'functools', 'itertools', 'pathlib', 'typing', 'dataclasses', 'enum', 'abc', 'contextlib', 'copy', 'pickle', 'sqlite3', 'urllib', 'http', 'threading', 'multiprocessing', 'asyncio', 'concurrent', 'queue', 'flet', 'fletx'}
        if name.lower() in common_modules:
            raise ValidationError(f"'{name}' conflicts with a common Python module name. Please choose a different {target_type} name.")

    @staticmethod
    def validate_path(path: str) -> None:
        """Validate a file path."""
        if not path:
            raise ValidationError('Path cannot be empty.')
        invalid_chars = '<>:"|?*'
        if any((char in path for char in invalid_chars)):
            raise ValidationError(f'Path contains invalid characters: {invalid_chars}')
        reserved_names = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
        path_parts = Path(path).parts
        for part in path_parts:
            if part.upper() in reserved_names:
                raise ValidationError(f"'{part}' is a reserved name and cannot be used in paths.")