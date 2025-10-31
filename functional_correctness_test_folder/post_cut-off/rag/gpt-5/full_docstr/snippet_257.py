from __future__ import annotations

import json
import os
from typing import Dict, Optional, Any


class TerminalTextStyles:
    """Manages loading, saving, and applying terminal text styles."""

    _RESET = "\033[0m"
    _BOLD = "\033[1m"
    _DIM = "\033[2m"
    _UNDERLINE = "\033[4m"
    _RED = "\033[31m"
    _GREEN = "\033[32m"
    _YELLOW = "\033[33m"
    _BLUE = "\033[34m"
    _MAGENTA = "\033[35m"
    _CYAN = "\033[36m"
    _WHITE = "\033[37m"

    def __init__(self, stylesheet_path: str = None):
        """
        Initializes the style manager.
        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        """
        self._stylesheet_path = os.path.expanduser(
            stylesheet_path if stylesheet_path else self._default_stylesheet_path()
        )
        self._styles: Dict[str, str] = self._get_default_styles()
        self.load_styles()

    def _default_stylesheet_path(self) -> str:
        jrdev_dir = os.environ.get("JRDEV_DIR")
        if not jrdev_dir:
            jrdev_dir = (
                globals().get("JRDEV_DIR")
                if isinstance(globals().get("JRDEV_DIR"), str)
                else None
            )
        if not jrdev_dir:
            jrdev_dir = os.path.join(os.path.expanduser("~"), ".jrdev")
        try:
            os.makedirs(jrdev_dir, exist_ok=True)
        except Exception:
            pass
        return os.path.join(jrdev_dir, "styles.json")

    def _default_for_name(self, name: str) -> str:
        n = name.lower()
        if "error" in n or "fail" in n:
            return f"{self._BOLD}{self._RED}"
        if "warn" in n:
            return f"{self._YELLOW}"
        if "success" in n or "ok" in n or "pass" in n:
            return f"{self._GREEN}"
        if "debug" in n:
            return f"{self._DIM}"
        if "title" in n or "header" in n:
            return f"{self._BOLD}{self._MAGENTA}"
        if "prompt" in n or "input" in n:
            return f"{self._BOLD}{self._BLUE}"
        if "emphasis" in n or "highlight" in n:
            return f"{self._UNDERLINE}"
        if "info" in n or "note" in n:
            return f"{self._CYAN}"
        return ""

    def _get_default_styles(self) -> Dict[str, str]:
        """Returns the default styles for each PrintType as a dictionary."""
        defaults: Dict[str, str] = {}
        try:
            PT = PrintType  # type: ignore[name-defined]
            members = list(PT) if hasattr(PT, "__iter__") else []
            for m in members:
                key = getattr(m, "name", str(m))
                defaults[key] = self._default_for_name(key)
        except NameError:
            pass
        return defaults

    def _ensure_parent_dir(self) -> None:
        parent = os.path.dirname(self._stylesheet_path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

    def load_styles(self) -> None:
        """Loads styles from the stylesheet file, merging them with defaults."""
        self._ensure_parent_dir()
        if not os.path.exists(self._stylesheet_path):
            return
        try:
            with open(self._stylesheet_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                merged = dict(self._styles)
                for k, v in data.items():
                    if isinstance(k, str) and isinstance(v, str):
                        merged[k] = v
                self._styles = merged
        except Exception:
            # If anything goes wrong, keep defaults
            pass

    def save_styles(self) -> bool:
        """Saves the current styles to the stylesheet file."""
        try:
            self._ensure_parent_dir()
            with open(self._stylesheet_path, "w", encoding="utf-8") as f:
                json.dump(self._styles, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def get_style(self, print_type: PrintType) -> str:
        """Gets the style string for a given PrintType."""
        key = getattr(print_type, "name", str(print_type))
        return self._styles.get(key, self._default_for_name(key))

    def set_style(self, print_type: PrintType, style_str: str) -> None:
        """Sets the style for a given PrintType."""
        key = getattr(print_type, "name", str(print_type))
        self._styles[key] = style_str
