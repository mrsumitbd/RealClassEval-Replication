
from typing import Dict, Optional
import os
import yaml
from pathlib import Path
from enum import Enum


class PrintType(Enum):
    pass  # Assuming PrintType is defined elsewhere


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
        self.styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            'INFO': '\033[94m',  # Blue
            'WARNING': '\033[93m',  # Yellow
            'ERROR': '\033[91m',  # Red
            'SUCCESS': '\033[92m',  # Green
            'DEBUG': '\033[90m',  # Gray
            'RESET': '\033[0m',  # Reset to default
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        if not os.path.exists(self.stylesheet_path):
            return
        with open(self.stylesheet_path, 'r') as f:
            try:
                custom_styles = yaml.safe_load(f) or {}
                self.styles.update(custom_styles)
            except yaml.YAMLError:
                pass

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, 'w') as f:
                yaml.dump(self.styles, f)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.name, self.styles['RESET'])

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.name] = style_str
