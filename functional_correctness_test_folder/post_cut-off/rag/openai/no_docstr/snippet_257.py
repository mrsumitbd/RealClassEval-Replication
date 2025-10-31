
import os
import yaml
from pathlib import Path
from typing import Dict, Any

# Try to import the real PrintType enum; fall back to a minimal stub if unavailable.
try:
    from jrdev.print_types import PrintType  # type: ignore
except Exception:  # pragma: no cover
    from enum import Enum

    class PrintType(Enum):
        INFO = "info"
        WARNING = "warning"
        ERROR = "error"
        DEBUG = "debug"
        SUCCESS = "success"
        # Add more types as needed


class TerminalTextStyles:
    """Manages loading, saving, and applying terminal text styles."""

    def __init__(self, stylesheet_path: str = None):
        """
        Initializes the style manager.

        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        """
        # Determine default path
        jrdev_dir = os.getenv("JRDEV_DIR", ".")
        self.stylesheet_path = (
            Path(stylesheet_path) if stylesheet_path else Path(
                jrdev_dir) / "styles.yaml"
        )
        self._styles: Dict[PrintType, str] = {}
        self.load_styles()

    def _get_default_styles(self) -> Dict[PrintType, str]:
        """Returns the default styles for each PrintType as a dictionary."""
        # ANSI escape codes for basic styling
        return {
            PrintType.INFO: "\033[94m",      # Bright blue
            PrintType.WARNING: "\033[93m",   # Bright yellow
            PrintType.ERROR: "\033[91m",     # Bright red
            PrintType.DEBUG: "\033[90m",     # Bright black (gray)
            PrintType.SUCCESS: "\033[92m",   # Bright green
        }

    def load_styles(self) -> None:
        """Loads styles from the stylesheet file, merging them with defaults."""
        defaults = self._get_default_styles()
        self._styles = defaults.copy()

        if self.stylesheet_path.exists():
            try:
                with open(self.stylesheet_path, "r", encoding="utf-8") as f:
                    data: Any = yaml.safe_load(f) or {}
                # Convert keys to PrintType if they are strings
                for key, value in data.items():
                    try:
                        pt = PrintType(key)
                    except ValueError:
                        # Skip unknown keys
                        continue
                    self._styles[pt] = str(value)
            except Exception:
                # If loading fails, keep defaults
                pass

    def save_styles(self) -> bool:
        """Saves the current styles to the stylesheet file."""
        try:
            # Ensure directory exists
            self.stylesheet_path.parent.mkdir(parents=True, exist_ok=True)
            # Convert keys to string for YAML
            data = {pt.value: style for pt, style in self._styles.items()}
            with open(self.stylesheet_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, default_flow_style=False)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        """Gets the style string for a given PrintType."""
        return self._styles.get(print_type, "")

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        """Sets the style for a given PrintType."""
        self._styles[print_type] = style_str
