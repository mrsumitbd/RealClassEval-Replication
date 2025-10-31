
import json
from typing import Dict
from enum import Enum


class PrintType(str, Enum):
    # Assuming PrintType is an Enum, you should define it according to your needs
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    # Add more PrintType as needed


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        self.stylesheet_path = stylesheet_path if stylesheet_path else 'styles.json'
        self.styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            PrintType.INFO.value: '\033[94m',  # Blue color
            PrintType.WARNING.value: '\033[93m',  # Yellow color
            PrintType.ERROR.value: '\033[91m',  # Red color
            # Add more default styles as needed
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        try:
            with open(self.stylesheet_path, 'r') as file:
                loaded_styles = json.load(file)
                self.styles.update(
                    {k: v for k, v in loaded_styles.items() if k in self.styles})
        except FileNotFoundError:
            pass  # File does not exist, use default styles

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            with open(self.stylesheet_path, 'w') as file:
                json.dump(self.styles, file)
            return True
        except Exception as e:
            print(f"Failed to save styles: {e}")
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        return self.styles.get(print_type.value, '')

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        self.styles[print_type.value] = style_str


# Example usage
if __name__ == "__main__":
    styles = TerminalTextStyles()
    print(styles.get_style(PrintType.INFO))
    styles.set_style(PrintType.INFO, '\033[92m')  # Green color
    print(styles.get_style(PrintType.INFO))
    styles.save_styles()
