
from typing import Dict, Optional
import json
from enum import Enum


class PrintType(Enum):
    HEADER = 'header'
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'


class TerminalTextStyles:

    def __init__(self, stylesheet_path: str = None):
        self.stylesheet_path = stylesheet_path
        self.styles = self._get_default_styles()
        if self.stylesheet_path:
            self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        return {
            'header': '\033[95m',
            'success': '\033[92m',
            'error': '\033[91m',
            'warning': '\033[93m',
            'info': '\033[94m'
        }

    def load_styles(self) -> None:
        try:
            with open(self.stylesheet_path, 'r') as file:
                self.styles.update(json.load(file))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_styles(self) -> bool:
        try:
            with open(self.stylesheet_path, 'w') as file:
                json.dump(self.styles, file, indent=4)
            return True
        except IOError:
            return False

    def get_style(self, print_type: PrintType) -> str:
        return self.styles.get(print_type.value, '')

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        self.styles[print_type.value] = style_str
