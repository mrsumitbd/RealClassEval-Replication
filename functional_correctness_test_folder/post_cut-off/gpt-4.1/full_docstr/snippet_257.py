
import os
import json
from typing import Dict

# Dummy PrintType enum for demonstration; replace with actual enum as needed.
from enum import Enum


class PrintType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    DEBUG = "DEBUG"


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
            jrdev_dir = os.environ.get(
                "JRDEV_DIR", os.path.expanduser("~/.jrdev"))
            os.makedirs(jrdev_dir, exist_ok=True)
            stylesheet_path = os.path.join(jrdev_dir, "terminal_styles.json")
        self.stylesheet_path = stylesheet_path
        self.styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.INFO.value:     "\033[0;37m",  # White
            PrintType.WARNING.value:  "\033[1;33m",  # Bold Yellow
            PrintType.ERROR.value:    "\033[1;31m",  # Bold Red
            PrintType.SUCCESS.value:  "\033[1;32m",  # Bold Green
            PrintType.DEBUG.value:    "\033[0;36m",  # Cyan
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        if os.path.exists(self.stylesheet_path):
            try:
                with open(self.stylesheet_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                # Merge loaded styles with defaults
                defaults = self._get_default_styles()
                for key in defaults:
                    if key in loaded and isinstance(loaded[key], str):
                        self.styles[key] = loaded[key]
                    else:
                        self.styles[key] = defaults[key]
            except Exception:
                self.styles = self._get_default_styles()
        else:
            self.styles = self._get_default_styles()

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, "w", encoding="utf-8") as f:
                json.dump(self.styles, f, indent=2)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        key = print_type.value if isinstance(
            print_type, Enum) else str(print_type)
        return self.styles.get(key, "")

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        key = print_type.value if isinstance(
            print_type, Enum) else str(print_type)
        self.styles[key] = style_str
