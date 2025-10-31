
from typing import Dict
import json
from enum import Enum


class PrintType(Enum):
    pass


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
            'INFO': '\033[94m',
            'WARNING': '\033[93m',
            'ERROR': '\033[91m',
            'SUCCESS': '\033[92m',
            'RESET': '\033[0m'
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        try:
            with open(self.stylesheet_path, 'r') as f:
                loaded_styles = json.load(f)
                for key, value in loaded_styles.items():
                    if key in self.styles:
                        self.styles[key] = value
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        if not self.stylesheet_path:
            return False
        try:
            with open(self.stylesheet_path, 'w') as f:
                json.dump(self.styles, f, indent=4)
            return True
        except:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.name, self.styles['RESET'])

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.name] = style_str
