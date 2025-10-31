
import json
import os
from pathlib import Path
from typing import Dict

# Assume PrintType is an Enum defined elsewhere; we treat it generically.
# If PrintType is not available, the code will still work with any hashable type.
try:
    from .print_type import PrintType  # Adjust import path as needed
except Exception:
    PrintType = str  # Fallback for type hinting

# Default directory for JRDEV configuration
JRDEV_DIR = os.getenv("JRDEV_DIR", str(Path.home() / ".jrdev"))


class TerminalTextStyles:
    """Manages loading, saving, and applying terminal text styles."""

    def __init__(self, stylesheet_path: str | None = None):
        """
        Initializes the style manager.

        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        """
        self.stylesheet_path = (
            Path(stylesheet_path) if stylesheet_path else Path(
                JRDEV_DIR) / "terminal_styles.json"
        )
        self.styles: Dict[str, str] = {}
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        """Returns the default styles for each PrintType as a dictionary."""
        # Default ANSI color codes for common log levels
        return {
            "DEBUG": "\033[34m",   # Blue
            "INFO": "\033[32m",    # Green
            "WARNING": "\033[33m",  # Yellow
            "ERROR": "\033[31m",   # Red
            "CRITICAL": "\033[35m",  # Magenta
            "RESET": "\033[0m",    # Reset
        }

    def load_styles(self) -> None:
        """Loads styles from the stylesheet file, merging them with defaults."""
        defaults = self._get_default_styles()
        if self.stylesheet_path.is_file():
            try:
                with self.stylesheet_path.open("r", encoding="utf-8") as f:
                    loaded = json.load(f)
                # Merge loaded styles over defaults
                merged = {**defaults, **{k: str(v) for k, v in loaded.items()}}
            except Exception:
                merged = defaults
        else:
            merged = defaults
        self.styles = merged

    def save_styles(self) -> bool:
        """Saves the current styles to the stylesheet file."""
        try:
            self.stylesheet_path.parent.mkdir(parents=True, exist_ok=True)
            with self.stylesheet_path.open("w", encoding="utf-8") as f:
                json.dump(self.styles, f, indent=4)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        """Gets the style string for a given PrintType."""
        key = str(print_type)
        return self.styles.get(key, self._get_default_styles().get(key, ""))

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        """Sets the style for a given PrintType."""
        self.styles[str(print_type)] = style_str
