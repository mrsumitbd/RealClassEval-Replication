
import json
import os
from typing import Dict

from enum import Enum


class PrintType(Enum):
    NORMAL = "NORMAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    SUCCESS = "SUCCESS"
    INFO = "INFO"


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        self.stylesheet_path = stylesheet_path
        self.styles = self._get_default_styles()
        if self.stylesheet_path:
            self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.NORMAL.value: "\033[0m",      # Reset
            PrintType.ERROR.value: "\033[91m",      # Red
            PrintType.WARNING.value: "\033[93m",    # Yellow
            PrintType.SUCCESS.value: "\033[92m",    # Green
            PrintType.INFO.value: "\033[94m",       # Blue
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        if not self.stylesheet_path or not os.path.isfile(self.stylesheet_path):
            return
        try:
            with open(self.stylesheet_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            # Merge loaded with defaults
            defaults = self._get_default_styles()
            for key in defaults:
                if key in loaded and isinstance(loaded[key], str):
                    self.styles[key] = loaded[key]
                else:
                    self.styles[key] = defaults[key]
        except Exception:
            # On error, keep defaults
            self.styles = self._get_default_styles()

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        if not self.stylesheet_path:
            return False
        try:
            with open(self.stylesheet_path, "w", encoding="utf-8") as f:
                json.dump(self.styles, f, indent=2)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.value, self._get_default_styles()[print_type.value])

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.value] = style_str
