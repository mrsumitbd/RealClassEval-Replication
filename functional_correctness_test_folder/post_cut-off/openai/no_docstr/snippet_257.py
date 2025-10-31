
import json
import os
from typing import Dict, Optional

# Assuming PrintType is an Enum defined elsewhere in the project.
# For the purpose of this implementation we import it if available,
# otherwise we create a minimal placeholder.
try:
    from .print_type import PrintType  # type: ignore
except Exception:
    from enum import Enum

    class PrintType(Enum):
        INFO = "info"
        WARNING = "warning"
        ERROR = "error"
        DEBUG = "debug"
        SUCCESS = "success"


class TerminalTextStyles:
    """
    Manages terminal text styles for different print types.
    Styles are stored as ANSI escape codes and can be persisted to a JSON file.
    """

    def __init__(self, stylesheet_path: Optional[str] = None):
        """
        Initialize the TerminalTextStyles instance.

        :param stylesheet_path: Optional path to a JSON file containing styles.
        """
        self.stylesheet_path: Optional[str] = stylesheet_path
        self._styles: Dict[PrintType, str] = {}
        if self.stylesheet_path and os.path.isfile(self.stylesheet_path):
            self.load_styles()
        else:
            self._styles = self._get_default_styles()

    def _get_default_styles(self) -> Dict[PrintType, str]:
        """
        Return a dictionary of default styles for each PrintType.

        :return: Dict mapping PrintType to ANSI escape code strings.
        """
        return {
            PrintType.INFO: "\033[94m",     # Blue
            PrintType.WARNING: "\033[93m",  # Yellow
            PrintType.ERROR: "\033[91m",    # Red
            PrintType.DEBUG: "\033[96m",    # Cyan
            PrintType.SUCCESS: "\033[92m",  # Green
        }

    def load_styles(self) -> None:
        """
        Load styles from the JSON file specified by stylesheet_path.
        If the file is missing or malformed, defaults are used.
        """
        if not self.stylesheet_path:
            self._styles = self._get_default_styles()
            return

        try:
            with open(self.stylesheet_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            loaded: Dict[PrintType, str] = {}
            for key, value in data.items():
                try:
                    enum_key = PrintType[key]
                    loaded[enum_key] = str(value)
                except KeyError:
                    # Ignore unknown keys
                    continue
            self._styles = loaded if loaded else self._get_default_styles()
        except Exception:
            # On any error, fall back to defaults
            self._styles = self._get_default_styles()

    def save_styles(self) -> bool:
        """
        Persist the current styles to the JSON file specified by stylesheet_path.

        :return: True if the file was written successfully, False otherwise.
        """
        if not self.stylesheet_path:
            return False

        try:
            data = {key.name: value for key, value in self._styles.items()}
            with open(self.stylesheet_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        """
        Retrieve the style string for a given PrintType.

        :param print_type: The PrintType for which to get the style.
        :return: The ANSI escape code string associated with the print_type.
        """
        return self._styles.get(print_type, self._get_default_styles().get(print_type, ""))

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        """
        Set or update the style string for a given PrintType.

        :param print_type: The PrintType to update.
        :param style_str: The ANSI escape code string to associate.
        """
        self._styles[print_type] = style_str
