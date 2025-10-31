from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional, Any


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        self.stylesheet_path: str = (
            stylesheet_path
            if stylesheet_path is not None
            else str(Path.home() / ".terminal_text_styles.json")
        )
        self.styles: Dict[str, str] = {}
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        defaults: Dict[str, str] = {}
        enum_members = self._get_print_type_members()

        base_defaults: Dict[str, str] = {
            "DEFAULT": "\033[0m",
            "INFO": "\033[36m",
            "WARNING": "\033[33m",
            "ERROR": "\033[31m",
            "SUCCESS": "\033[32m",
            "DEBUG": "\033[35m",
            "TITLE": "\033[1m",
        }

        if not enum_members:
            # Fallback when PrintType isn't available
            return {
                "DEFAULT": "\033[0m",
                "INFO": "\033[36m",
                "WARNING": "\033[33m",
                "ERROR": "\033[31m",
                "SUCCESS": "\033[32m",
                "DEBUG": "\033[35m",
                "TITLE": "\033[1m",
            }

        for name in enum_members:
            defaults[name] = base_defaults.get(name, "\033[0m")
        return defaults

    def _get_print_type_members(self) -> Optional[list[str]]:
        try:
            # noqa: F821 - PrintType is a forward reference provided by the host environment
            PT = PrintType  # type: ignore[name-defined]
        except Exception:
            return None
        try:
            import enum

            # type: ignore[arg-type]
            if isinstance(PT, type) and issubclass(PT, enum.Enum):
                # type: ignore[iteration-over-annotated-type]
                return [member.name for member in PT]
        except Exception:
            return None
        return None

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        defaults = self._get_default_styles()
        loaded: Dict[str, Any] = {}

        path = Path(self.stylesheet_path)
        if path.is_file():
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        loaded = {str(k): str(v) for k, v in data.items()}
            except Exception:
                loaded = {}

        merged: Dict[str, str] = {}
        # Ensure defaults for known keys
        for k, v in defaults.items():
            merged[k] = str(loaded.get(k, v))
        # Preserve any additional keys that may exist in the file
        for k, v in loaded.items():
            if k not in merged:
                merged[k] = str(v)

        self.styles = merged

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            path = Path(self.stylesheet_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as f:
                json.dump(self.styles, f, ensure_ascii=False,
                          indent=2, sort_keys=True)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        '''Gets the style string for a given PrintType.'''
        key = self._print_type_key(print_type)
        return self.styles.get(key, "\033[0m")

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        if not isinstance(style_str, str):
            raise TypeError("style_str must be a string")
        key = self._print_type_key(print_type)
        self.styles[key] = style_str

    def _print_type_key(self, print_type: Any) -> str:
        try:
            import enum

            if isinstance(print_type, enum.Enum):
                return print_type.name
        except Exception:
            pass
        return getattr(print_type, "name", str(print_type))
