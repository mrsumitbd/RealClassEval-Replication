
from typing import Dict, Optional
from dbt.exceptions import DbtInternalError
from dbt.events.base_types import PrintType
import os
import json


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: Optional[str] = None):
        '''
        Initializes the style manager.
        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        '''
        self.stylesheet_path = stylesheet_path or os.path.join(
            os.environ.get('JRDEV_DIR', ''), 'styles.json')
        self.styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.Error: '\033[91m',  # Red
            PrintType.Warn: '\033[93m',   # Yellow
            PrintType.Info: '\033[0m',    # Default
            PrintType.Debug: '\033[90m',  # Gray
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        try:
            with open(self.stylesheet_path, 'r') as f:
                loaded_styles = json.load(f)
                self.styles.update(
                    {k: v for k, v in loaded_styles.items() if k in self.styles})
        except FileNotFoundError:
            pass
        except json.JSONDecodeError as e:
            raise DbtInternalError(
                f'Failed to load styles from {self.stylesheet_path}: {e}')

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, 'w') as f:
                json.dump(self.styles, f)
            return True
        except Exception as e:
            raise DbtInternalError(
                f'Failed to save styles to {self.stylesheet_path}: {e}')

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.value, '')

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.value] = style_str
