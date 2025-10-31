
from typing import Dict
import json
from enum import Enum


class PrintType(Enum):
    HEADER = "header"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"


class TerminalTextStyles:

    def __init__(self, stylesheet_path: str = None):
        self.stylesheet_path = stylesheet_path
        self.styles = self._get_default_styles()
        if stylesheet_path:
            self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        return {
            PrintType.HEADER.value: "\033[95m",
            PrintType.SUCCESS.value: "\033[92m",
            PrintType.WARNING.value: "\033[93m",
            PrintType.ERROR.value: "\033[91m",
            PrintType.INFO.value: "\033[94m"
        }

    def load_styles(self) -> None:
        try:
            with open(self.stylesheet_path, 'r') as f:
                loaded_styles = json.load(f)
                for key, value in loaded_styles.items():
                    if key in self.styles:
                        self.styles[key] = value
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_styles(self) -> bool:
        if not self.stylesheet_path:
            return False
        try:
            with open(self.stylesheet_path, 'w') as f:
                json.dump(self.styles, f, indent=4)
            return True
        except:
            return False

    def get_style(self, print_type: PrintType) -> str:
        return self.styles.get(print_type.value, "")

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        self.styles[print_type.value] = style_str
