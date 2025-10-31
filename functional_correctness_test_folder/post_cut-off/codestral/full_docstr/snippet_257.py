
import os
from typing import Dict
from enum import Enum


class PrintType(Enum):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SUCCESS = 'success'


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        '''
        Initializes the style manager.
        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        '''
        self.stylesheet_path = stylesheet_path or os.path.join(
            os.getenv('JRDEV_DIR', ''), 'styles.json')
        self.styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.INFO.value: '\033[94m',    # Blue
            PrintType.WARNING.value: '\033[93m',  # Yellow
            PrintType.ERROR.value: '\033[91m',    # Red
            PrintType.SUCCESS.value: '\033[92m',  # Green
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        try:
            with open(self.stylesheet_path, 'r') as f:
                custom_styles = json.load(f)
                self.styles.update(custom_styles)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, 'w') as f:
                json.dump(self.styles, f, indent=4)
            return True
        except (IOError, TypeError):
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.value, '')

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.value] = style_str
