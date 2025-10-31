
import json
import os
from typing import Dict, Optional

from enum import Enum


class PrintType(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    DEBUG = "debug"


class TerminalTextStyles:

    def __init__(self, stylesheet_path: str = None):
        self.stylesheet_path = stylesheet_path
        self.styles: Dict[str, str] = self._get_default_styles()
        if self.stylesheet_path:
            self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        return {
            "info": "\033[94m",     # Blue
            "warning": "\033[93m",  # Yellow
            "error": "\033[91m",    # Red
            "success": "\033[92m",  # Green
            "debug": "\033[90m",    # Grey
        }

    def load_styles(self) -> None:
        if self.stylesheet_path and os.path.isfile(self.stylesheet_path):
            try:
                with open(self.stylesheet_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        for k, v in data.items():
                            if k in self.styles:
                                self.styles[k] = v
            except Exception:
                pass

    def save_styles(self) -> bool:
        if not self.stylesheet_path:
            return False
        try:
            with open(self.stylesheet_path, "w", encoding="utf-8") as f:
                json.dump(self.styles, f, indent=2)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        return self.styles.get(print_type.value, "")

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        self.styles[print_type.value] = style_str
