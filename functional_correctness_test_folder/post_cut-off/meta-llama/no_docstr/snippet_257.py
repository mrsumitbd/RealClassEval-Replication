
from typing import Dict
from enum import Enum
import json
import os


class PrintType(str, Enum):
    HEADER = 'header'
    OKBLUE = 'okblue'
    OKCYAN = 'okcyan'
    OKGREEN = 'okgreen'
    WARNING = 'warning'
    FAIL = 'fail'
    ENDC = 'endc'
    BOLD = 'bold'
    UNDERLINE = 'underline'


class TerminalTextStyles:

    def __init__(self, stylesheet_path: str = None):
        self.stylesheet_path = stylesheet_path if stylesheet_path else os.path.join(
            os.path.expanduser('~'), '.terminal_styles.json')
        self.styles = self._get_default_styles()
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        return {
            PrintType.HEADER.value: '\033[95m',
            PrintType.OKBLUE.value: '\033[94m',
            PrintType.OKCYAN.value: '\033[96m',
            PrintType.OKGREEN.value: '\033[92m',
            PrintType.WARNING.value: '\033[93m',
            PrintType.FAIL.value: '\033[91m',
            PrintType.ENDC.value: '\033[0m',
            PrintType.BOLD.value: '\033[1m',
            PrintType.UNDERLINE.value: '\033[4m'
        }

    def load_styles(self) -> None:
        if os.path.exists(self.stylesheet_path):
            try:
                with open(self.stylesheet_path, 'r') as file:
                    self.styles = json.load(file)
            except json.JSONDecodeError:
                pass

    def save_styles(self) -> bool:
        try:
            with open(self.stylesheet_path, 'w') as file:
                json.dump(self.styles, file)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        return self.styles.get(print_type.value, '')

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        self.styles[print_type.value] = style_str
        self.save_styles()
