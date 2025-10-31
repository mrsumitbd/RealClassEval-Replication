
from typing import Dict, Optional
import json
from enum import Enum


class PrintType(Enum):
    HEADER = 'header'
    BODY = 'body'
    FOOTER = 'footer'
    ERROR = 'error'
    SUCCESS = 'success'


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
            PrintType.HEADER.value: '\033[1;34m',  # Bold blue
            PrintType.BODY.value: '\033[0m',       # Reset
            PrintType.FOOTER.value: '\033[1;32m',  # Bold green
            PrintType.ERROR.value: '\033[1;31m',   # Bold red
            PrintType.SUCCESS.value: '\033[1;32m'  # Bold green
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        try:
            with open(self.stylesheet_path, 'r') as file:
                loaded_styles = json.load(file)
                self.styles.update(loaded_styles)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        if not self.stylesheet_path:
            return False
        try:
            with open(self.stylesheet_path, 'w') as file:
                json.dump(self.styles, file, indent=4)
            return True
        except IOError:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.value, '')

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.value] = style_str
