
import json
from enum import Enum
from typing import Dict


class PrintType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


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
            PrintType.INFO.value: "\033[94m",  # Blue
            PrintType.WARNING.value: "\033[93m",  # Yellow
            PrintType.ERROR.value: "\033[91m",  # Red
            PrintType.SUCCESS.value: "\033[92m",  # Green
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        try:
            with open(self.stylesheet_path, 'r') as file:
                custom_styles = json.load(file)
                self.styles.update(custom_styles)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, 'w') as file:
                json.dump(self.styles, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.value, "")

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.value] = style_str
