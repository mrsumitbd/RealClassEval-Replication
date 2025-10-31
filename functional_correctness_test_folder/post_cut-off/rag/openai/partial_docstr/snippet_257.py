
import os
import yaml
from pathlib import Path
from typing import Dict, Optional

# A minimal PrintType enum for demonstration purposes.
# In real usage this should be imported from the appropriate module.
try:
    from my_project.print_types import PrintType  # type: ignore
except Exception:
    from enum import Enum

    class PrintType(Enum):
        INFO = "info"
        WARNING = "warning"
        ERROR = "error"
        DEBUG = "debug"
        SUCCESS = "success"


class TerminalTextStyles:
    """Manages loading, saving, and applying terminal text styles."""

    def __init__(self, stylesheet_path: Optional[str] = None):
        """
        Initializes the style manager.

        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        """
        if stylesheet_path is None:
            jrdev_dir = os.getenv("JRDEV_DIR", ".")
            stylesheet_path = Path(jrdev_dir) / "terminal_styles.yml"
        self.stylesheet_path = Path(stylesheet_path).expanduser().resolve()
        self._styles: Dict[PrintType, str] = {}
        self.load_styles()

    def _get_default_styles(self) -> Dict[PrintType, str]:
        """Returns the default styles for each PrintType as a dictionary."""
        return {
            PrintType.INFO: "\033[94m",      # bright blue
            PrintType.WARNING: "\033[93m",   # bright yellow
            PrintType.ERROR: "\033[91m",     # bright red
            PrintType.DEBUG: "\033[90m",     # bright black (gray)
            PrintType.SUCCESS: "\033[92m",   # bright green
        }

    def load_styles(self) -> None:
        """Loads styles from the stylesheet file, merging them with defaults."""
        defaults = self._get_default_styles()
        if self.stylesheet_path.exists():
            try:
                with open(self.stylesheet_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                # Convert keys to PrintType
                for key, value in data.items():
                    try:
                        pt = PrintType(key)
                        defaults[pt] = value
                    except ValueError:
                        # Unknown key; ignore
                        pass
            except Exception:
                # If loading fails, fall back to defaults
                pass
        # Ensure all defaults are present
        self._styles = defaults

    def save_styles(self) -> bool:
        """Saves the current styles to the stylesheet file."""
        try:
            # Convert keys to string for YAML
            data = {pt.value: style for pt, style in self._styles.items()}
            # Ensure directory exists
            self.stylesheet_path.parent.mkdir(parents=True, exist_ok=True)
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
