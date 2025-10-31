
from typing import Dict
import os
import yaml
from pathlib import Path
from .print_type import PrintType


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        '''
        Initializes the style manager.
        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        '''
        self.stylesheet_path = stylesheet_path if stylesheet_path else os.path.join(
            os.getenv('JRDEV_DIR'), 'terminal_styles.yml')
        self._styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.HEADER: '\033[1;36m',  # Bold Cyan
            PrintType.SUCCESS: '\033[1;32m',  # Bold Green
            PrintType.WARNING: '\033[1;33m',  # Bold Yellow
            PrintType.ERROR: '\033[1;31m',    # Bold Red
            PrintType.INFO: '\033[1;37m',     # Bold White
            PrintType.DEBUG: '\033[0;35m',    # Purple
            PrintType.PLAIN: '\033[0m',       # Reset
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
            Path(self.stylesheet_path).parent.mkdir(
                parents=True, exist_ok=True)
            with open(self.stylesheet_path, 'w') as f:
                yaml.dump(self._styles, f)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self._styles.get(print_type.name, self._styles[PrintType.PLAIN.name])

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self._styles[print_type.name] = style_str
