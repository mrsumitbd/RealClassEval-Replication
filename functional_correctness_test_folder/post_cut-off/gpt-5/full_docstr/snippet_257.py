from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional, Any


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        '''
        Initializes the style manager.
        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        '''
        self._styles: Dict[str, str] = {}
        self.stylesheet_path = self._resolve_stylesheet_path(stylesheet_path)
        self.load_styles()

    def _resolve_stylesheet_path(self, stylesheet_path: Optional[str]) -> Path:
        if stylesheet_path:
            return Path(stylesheet_path).expanduser().resolve()
        base_dir = os.environ.get("JRDEV_DIR")
        if base_dir:
            base = Path(base_dir).expanduser()
        else:
            base = Path.home() / ".jrdev"
        return (base / "terminal_styles.json").resolve()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        return {
            # Fallback/default style
            "DEFAULT": "",
            # Common print types
            "INFO": "\033[36m",     # Cyan
            "WARNING": "\033[33m",  # Yellow
            "ERROR": "\033[31m",    # Red
            "SUCCESS": "\033[32m",  # Green
            "DEBUG": "\033[35m",    # Magenta
            "TITLE": "\033[1m",     # Bold
            "PROMPT": "\033[34m",   # Blue
        }

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        styles: Dict[str, str] = dict(self._get_default_styles())

        path = self.stylesheet_path
        if path.is_file():
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(k, str) and isinstance(v, str):
                            styles[k] = v
            except Exception:
                # Keep defaults if reading fails
                pass

        self._styles = styles

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            path = self.stylesheet_path
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as f:
                json.dump(self._styles, f, indent=2, sort_keys=True)
            return True
        except Exception:
            return False

    def _key_from_print_type(self, print_type: Any) -> str:
        # Supports Enum-like with .name, string keys, or falls back to str(obj)
        if hasattr(print_type, "name"):
            name = getattr(print_type, "name")
            if isinstance(name, str):
                return name
        if isinstance(print_type, str):
            return print_type
        return str(print_type)

    def get_style(self, print_type) -> str:
        '''Gets the style string for a given PrintType.'''
        key = self._key_from_print_type(print_type)
        return self._styles.get(key, self._styles.get("DEFAULT", ""))

    def set_style(self, print_type, style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        key = self._key_from_print_type(print_type)
        if not isinstance(style_str, str):
            raise TypeError("style_str must be a string")
        self._styles[key] = style_str
