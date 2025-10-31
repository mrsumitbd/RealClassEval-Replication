from typing import Dict, Optional
import os
import json

# Assume PrintType is an Enum defined elsewhere
try:
    from .types import PrintType
except ImportError:
    from enum import Enum

    class PrintType(Enum):
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"
        SUCCESS = "SUCCESS"
        DEBUG = "DEBUG"

JRDEV_DIR = os.path.expanduser("~/.jrdev")
DEFAULT_STYLESHEET_FILENAME = "terminal_styles.json"


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        '''
        Initializes the style manager.
        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        '''
        if stylesheet_path is None:
            if not os.path.exists(JRDEV_DIR):
                os.makedirs(JRDEV_DIR, exist_ok=True)
            stylesheet_path = os.path.join(
                JRDEV_DIR, DEFAULT_STYLESHEET_FILENAME)
        self.stylesheet_path = stylesheet_path
        self._styles: Dict[str, str] = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.INFO.value: "\033[0m",         # Default (reset)
            PrintType.WARNING.value: "\033[33m",     # Yellow
            PrintType.ERROR.value: "\033[31m",       # Red
            PrintType.SUCCESS.value: "\033[32m",     # Green
            PrintType.DEBUG.value: "\033[36m",       # Cyan
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        if os.path.exists(self.stylesheet_path):
            try:
                with open(self.stylesheet_path, "r") as f:
                    loaded = json.load(f)
                # Merge loaded styles with defaults
                defaults = self._get_default_styles()
                for k, v in loaded.items():
                    if k in defaults:
                        defaults[k] = v
                self._styles = defaults
            except Exception:
                self._styles = self._get_default_styles()
        else:
            self._styles = self._get_default_styles()

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, "w") as f:
                json.dump(self._styles, f, indent=2)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self._styles.get(print_type.value, "\033[0m")

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self._styles[print_type.value] = style_str
