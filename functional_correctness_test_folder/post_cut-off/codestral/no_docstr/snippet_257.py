
from typing import Dict
import json
import os


class PrintType:
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


class TerminalTextStyles:

    def __init__(self, stylesheet_path: str = None):

        self.stylesheet_path = stylesheet_path
        self.styles = self._get_default_styles()
        if self.stylesheet_path is not None:
            self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:

        return {
            PrintType.INFO: "\033[94m",  # Blue
            PrintType.WARNING: "\033[93m",  # Yellow
            PrintType.ERROR: "\033[91m",  # Red
            PrintType.SUCCESS: "\033[92m"  # Green
        }

    def load_styles(self) -> None:

        if os.path.exists(self.stylesheet_path):
            with open(self.stylesheet_path, 'r') as f:
                self.styles = json.load(f)

    def save_styles(self) -> bool:

        try:
            with open(self.stylesheet_path, 'w') as f:
                json.dump(self.styles, f)
            return True
        except Exception as e:
            print(f"Error saving styles: {e}")
            return False

    def get_style(self, print_type: PrintType) -> str:

        return self.styles.get(print_type, "")

    def set_style(self, print_type: PrintType, style_str: str) -> None:

        self.styles[print_type] = style_str
