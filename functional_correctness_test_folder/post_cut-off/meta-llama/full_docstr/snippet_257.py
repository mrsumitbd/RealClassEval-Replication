
import os
import json
from typing import Dict
from enum import Enum

# Assuming PrintType is an Enum


class PrintType(Enum):
    # Example values, replace with actual PrintType values
    NORMAL = 1
    WARNING = 2
    ERROR = 3


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        '''
        Initializes the style manager.
        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        '''
        self.styles = {}
        self.stylesheet_path = stylesheet_path or os.path.join(
            os.environ.get('JRDEV_DIR', ''), 'terminal_styles.json')
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.NORMAL.name: '\033[0m',  # Default style
            PrintType.WARNING.name: '\033[93m',  # Yellow color for warnings
            PrintType.ERROR.name: '\033[91m',  # Red color for errors
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        default_styles = self._get_default_styles()
        try:
            with open(self.stylesheet_path, 'r') as file:
                loaded_styles = json.load(file)
                self.styles = {**default_styles, **loaded_styles}
        except (FileNotFoundError, json.JSONDecodeError):
            self.styles = default_styles

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, 'w') as file:
                json.dump(self.styles, file, indent=4)
            return True
        except Exception as e:
            print(f"Failed to save styles: {e}")
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.name, '')

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.name] = style_str


# Example usage
if __name__ == "__main__":
    style_manager = TerminalTextStyles()
    print(style_manager.get_style(PrintType.NORMAL))
    # Set normal style to green
    style_manager.set_style(PrintType.NORMAL, '\033[92m')
    print(style_manager.get_style(PrintType.NORMAL))
    style_manager.save_styles()
