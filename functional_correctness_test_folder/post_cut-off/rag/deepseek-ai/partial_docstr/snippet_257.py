
from typing import Dict
import os
import yaml
from pathlib import Path
from enum import Enum


class PrintType(Enum):
    pass  # Assuming PrintType is an Enum defined elsewhere


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
            os.getenv('JRDEV_DIR', ''), 'terminal_styles.yml')
        self._styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.INFO.name: '\033[94m',  # Blue
            PrintType.SUCCESS.name: '\033[92m',  # Green
            PrintType.WARNING.name: '\033[93m',  # Yellow
            PrintType.ERROR.name: '\033[91m',  # Red
            PrintType.DEBUG.name: '\033[90m',  # Gray
            PrintType.RESET.name: '\033[0m',  # Reset
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        if not os.path.exists(self.stylesheet_path):
            return
        with open(self.stylesheet_path, 'r') as f:
            custom_styles = yaml.safe_load(f) or {}
        for key, value in custom_styles.items():
            if key in self._styles:
                self._styles[key] = value

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, 'w') as f:
                yaml.dump(self._styles, f)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self._styles.get(print_type.name, '')

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self._styles[print_type.name] = style_str
