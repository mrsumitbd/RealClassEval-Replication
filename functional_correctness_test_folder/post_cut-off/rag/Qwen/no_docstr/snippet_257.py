
import os
import json
from typing import Dict, Optional


class PrintType:
    # Assuming PrintType is an enum or a class with predefined types
    # For demonstration, let's define some basic types
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
        self.JRDEV_DIR = os.getenv('JRDEV_DIR', os.path.expanduser('~/.jrdev'))
        self.stylesheet_path = stylesheet_path or os.path.join(
            self.JRDEV_DIR, 'styles.json')
        self.styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.INFO: '\033[34m',    # Blue
            PrintType.WARNING: '\033[33m',  # Yellow
            PrintType.ERROR: '\033[31m',   # Red
            PrintType.SUCCESS: '\033[32m'  # Green
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        if os.path.exists(self.stylesheet_path):
            with open(self.stylesheet_path, 'r') as file:
                loaded_styles = json.load(file)
                self.styles.update(loaded_styles)

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            os.makedirs(os.path.dirname(self.stylesheet_path), exist_ok=True)
            with open(self.stylesheet_path, 'w') as file:
                json.dump(self.styles, file, indent=4)
            return True
        except Exception as e:
            print(f"Failed to save styles: {e}")
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type, '')

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type] = style_str
        self.save_styles()
