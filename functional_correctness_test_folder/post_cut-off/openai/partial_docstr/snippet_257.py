
import json
import os
from pathlib import Path
from typing import Dict

# A minimal PrintType enum for demonstration purposes.
# In real usage, replace this with the actual enum definition.
try:
    from enum import Enum

    class PrintType(Enum):
        INFO = "info"
        WARN = "warn"
        ERROR = "error"
        DEBUG = "debug"
        RESET = "reset"
except Exception:
    # Fallback if enum is not available
    PrintType = str


class TerminalTextStyles:
    """Manages loading, saving, and applying terminal text styles."""

    def __init__(self, stylesheet_path: str | None = None):
        """
        Initialize the TerminalTextStyles instance.

        Parameters
        ----------
        stylesheet_path : str | None, optional
            Path to the JSON file containing custom styles. If None,
            a default path ``~/.terminal_text_styles.json`` is used.
        """
        self.stylesheet_path = (
            Path(stylesheet_path).expanduser() if stylesheet_path else Path(
                "~/.terminal_text_styles.json").expanduser()
        )
        self._styles: Dict[str, str] = {}
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        """Returns the default styles for each PrintType as a dictionary."""
        return {
            PrintType.INFO.value: "\033[92m",   # green
            PrintType.WARN.value: "\033[93m",   # yellow
            PrintType.ERROR.value: "\033[91m",  # red
            PrintType.DEBUG.value: "\033[94m",  # blue
            PrintType.RESET.value: "\033[0m",   # reset
        }

    def load_styles(self) -> None:
        """
        Loads styles from the stylesheet file, merging them with defaults.

        If the file does not exist, defaults are used.
        """
        defaults = self._get_default_styles()
        if self.stylesheet_path.is_file():
            try:
                with self.stylesheet_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    # Merge custom styles over defaults
                    merged = {**defaults, **{k: v for k,
                                             v in data.items() if isinstance(v, str)}}
                    self._styles = merged
                else:
                    self._styles = defaults
            except Exception:
                # On any error, fall back to defaults
                self._styles = defaults
        else:
            self._styles = defaults

    def save_styles(self) -> bool:
        """
        Saves the current styles to the stylesheet file.

        Returns
        -------
        bool
            True if the file was written successfully, False otherwise.
        """
        try:
            # Ensure parent directory exists
            self.stylesheet_path.parent.mkdir(parents=True, exist_ok=True)
            with self.stylesheet_path.open("w", encoding="utf-8") as f:
                json.dump(self._styles, f, indent=4, sort_keys=True)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        """
        Gets the style string for a given PrintType.

        Parameters
        ----------
        print_type : PrintType
            The type of print for which to retrieve the style.

        Returns
        -------
        str
            The ANSI escape code string for the requested type.
        """
        key = print_type.value if hasattr(
            print_type, "value") else str(print_type)
        return self._styles.get(key, "")

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        """
        Sets the style for a given PrintType.

        Parameters
        ----------
        print_type : PrintType
            The type of print to style.
        style_str : str
            The ANSI escape code string to associate with the type.
        """
        key = print_type.value if hasattr(
            print_type, "value") else str(print_type)
        self._styles[key] = style_str
