from typing import Dict, Optional
from pathlib import Path
import os
import json

try:
    # Optional: if yaml is available and the file extension is .yml/.yaml, we can read it.
    import yaml  # type: ignore
    _YAML_AVAILABLE = True
except Exception:
    _YAML_AVAILABLE = False


class TerminalTextStyles:
    """Manages loading, saving, and applying terminal text styles."""

    def __init__(self, stylesheet_path: str = None):
        """
        Initializes the style manager.
        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        """
        if stylesheet_path is not None:
            self._path = Path(stylesheet_path)
        else:
            jrdev_dir = os.environ.get("JRDEV_DIR", None)
            if not jrdev_dir:
                jrdev_dir = str(Path.home() / ".jrdev")
            self._path = Path(jrdev_dir) / "terminal_styles.json"

        self._styles: Dict[str, str] = {}
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        """Returns the default styles for each PrintType as a dictionary."""
        # ANSI style examples; keys correspond to common PrintType names.
        # Unknown PrintTypes will fall back to "" (no styling).
        return {
            "INFO": "\033[36m",     # Cyan
            "WARN": "\033[33m",     # Yellow
            "WARNING": "\033[33m",  # Alias of WARN
            "ERROR": "\033[31m",    # Red
            "SUCCESS": "\033[32m",  # Green
            "DEBUG": "\033[35m",    # Magenta
            "TITLE": "\033[1m",     # Bold
            "PROMPT": "\033[34m",   # Blue
            "PRIMARY": "\033[97m",  # Bright White
            "SECONDARY": "\033[90m"  # Bright Black (gray)
        }

    def _coerce_print_type_name(self, print_type) -> str:
        # Try .name (Enum-like), else string conversion.
        name = getattr(print_type, "name", None)
        if isinstance(name, str):
            return name
        if isinstance(print_type, str):
            return print_type
        return str(print_type)

    def load_styles(self) -> None:
        """Loads styles from the stylesheet file, merging them with defaults."""
        self._styles = dict(self._get_default_styles())

        if not self._path.exists() or not self._path.is_file():
            return

        try:
            loaded: Dict[str, str] = {}
            suffix = self._path.suffix.lower()
            if suffix in {".yml", ".yaml"} and _YAML_AVAILABLE:
                with self._path.open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
            else:
                with self._path.open("r", encoding="utf-8") as f:
                    data = json.load(f)

            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(k, str) and isinstance(v, str):
                        loaded[k] = v

            # Merge, file values override defaults
            self._styles.update(loaded)
        except Exception:
            # On any error, keep defaults.
            pass

    def save_styles(self) -> bool:
        """Saves the current styles to the stylesheet file."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            suffix = self._path.suffix.lower()
            if suffix in {".yml", ".yaml"} and _YAML_AVAILABLE:
                with self._path.open("w", encoding="utf-8") as f:
                    yaml.safe_dump(self._styles, f,
                                   default_flow_style=False, sort_keys=True)
            else:
                with self._path.open("w", encoding="utf-8") as f:
                    json.dump(self._styles, f, indent=2,
                              ensure_ascii=False, sort_keys=True)
            return True
        except Exception:
            return False

    def get_style(self, print_type) -> str:
        """Gets the style string for a given PrintType."""
        name = self._coerce_print_type_name(print_type)
        return self._styles.get(name, "")

    def set_style(self, print_type, style_str: str) -> None:
        """Sets the style for a given PrintType."""
        name = self._coerce_print_type_name(print_type)
        if not isinstance(style_str, str):
            raise TypeError("style_str must be a string")
        self._styles[name] = style_str
