
import os
import json
from typing import Dict, Optional
from enum import Enum


class PrintType(Enum):
    pass


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        '''
        Initializes the style manager.
        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        '''
        self.stylesheet_path = stylesheet_path
        if self.stylesheet_path is None:
            jrdev_dir = os.getenv('JRDEV_DIR', os.path.expanduser('~'))
            self.stylesheet_path = os.path.join(
                jrdev_dir, 'terminal_styles.json')
        self.styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            'INFO': '\033[94m',    # Blue
            'SUCCESS': '\033[92m',  # Green
            'WARNING': '\033[93m',  # Yellow
            'ERROR': '\033[91m',   # Red
            'RESET': '\033[0m'     # Reset
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        if os.path.exists(self.stylesheet_path):
            with open(self.stylesheet_path, 'r') as f:
                try:
                    loaded_styles = json.load(f)
                    self.styles.update(loaded_styles)
                except json.JSONDecodeError:
                    pass

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, 'w') as f:
                json.dump(self.styles, f, indent=4)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.name, self.styles['RESET'])

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.name] = style_str
