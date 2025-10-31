
from typing import Dict, Optional
from dbt.exceptions import DbtInternalError
from dbt.events.base import PrintType
import os
import yaml


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
            os.environ.get('JRDEV_DIR', ''), 'styles.yml')
        self.styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.SECTION: '\033[1;32m',  # Green
            PrintType.SUBSECTION: '\033[1;34m',  # Blue
            PrintType.ERROR: '\033[1;31m',  # Red
            PrintType.WARNING: '\033[1;33m',  # Yellow
            PrintType.INFO: '\033[0m',  # Default
            PrintType.DEBUG: '\033[90m',  # Grey
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        if os.path.exists(self.stylesheet_path):
            try:
                with open(self.stylesheet_path, 'r') as f:
                    loaded_styles = yaml.safe_load(f) or {}
                    self.styles.update(
                        {k: v for k, v in loaded_styles.items() if k in self.styles})
            except yaml.YAMLError:
                raise DbtInternalError(
                    f'Failed to parse stylesheet file: {self.stylesheet_path}')

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, 'w') as f:
                yaml.dump(self.styles, f)
            return True
        except Exception as e:
            raise DbtInternalError(
                f'Failed to save stylesheet file: {self.stylesheet_path}') from e

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.value, '')

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.value] = style_str
