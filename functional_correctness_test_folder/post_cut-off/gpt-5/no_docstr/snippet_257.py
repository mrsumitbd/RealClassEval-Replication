from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict


class TerminalTextStyles:
    def __init__(self, stylesheet_path: str = None):
        self._path = Path(stylesheet_path) if stylesheet_path else Path.home(
        ) / ".terminal_text_styles.json"
        self._styles: Dict["PrintType", str] = {}
        self._init_defaults()
        self.load_styles()

    def _init_defaults(self) -> None:
        defaults = self._get_default_styles()
        try:
            # Map default dict[str, str] into Dict[PrintType, str]
            for name, style in defaults.items():
                try:
                    self._styles[type(next(iter(self._iterate_print_types())))[
                        name]] = style  # type: ignore
                except Exception:
                    # Fallback when PrintType is not iterable yet; try direct enum access
                    try:
                        self._styles[PrintType[name]] = style  # type: ignore
                    except Exception:
                        pass
        except Exception:
            # Last resort: keep an empty style map, relying on load_styles or explicit set_style
            self._styles = {}

    def _iterate_print_types(self):
        # Helper to iterate enum members if available
        try:
            for member in PrintType:  # type: ignore
                yield member
        except Exception:
            return
            yield  # make it a generator

    def _get_default_styles(self) -> Dict[str, str]:
        return {
            "INFO": "\033[94m",
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "SUCCESS": "\033[92m",
            "DEBUG": "\033[90m",
            "DEFAULT": "\033[0m",
        }

    def load_styles(self) -> None:
        try:
            if not self._path.exists() or not self._path.is_file():
                return
            with self._path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return
            for key, val in data.items():
                if not isinstance(key, str) or not isinstance(val, str):
                    continue
                try:
                    pt = PrintType[key]  # type: ignore
                except Exception:
                    continue
                self._styles[pt] = val
        except Exception:
            # Ignore load errors and keep current styles
            return

    def save_styles(self) -> bool:
        try:
            serializable: Dict[str, str] = {}
            # Prefer saving all known enum members; fallback to currently set keys
            try:
                for pt in PrintType:  # type: ignore
                    style = self._styles.get(pt)
                    if isinstance(style, str):
                        serializable[pt.name] = style
            except Exception:
                for k, v in self._styles.items():
                    try:
                        name = k.name  # type: ignore
                    except Exception:
                        continue
                    if isinstance(v, str):
                        serializable[name] = v

            self._path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = self._path.with_suffix(self._path.suffix + ".tmp")
            with tmp_path.open("w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2, sort_keys=True)
            os.replace(tmp_path, self._path)
            return True
        except Exception:
            try:
                if "tmp_path" in locals() and Path(tmp_path).exists():
                    Path(tmp_path).unlink(missing_ok=True)  # type: ignore
            except Exception:
                pass
            return False

    def get_style(self, print_type: "PrintType") -> str:
        return self._styles.get(print_type, "")

    def set_style(self, print_type: "PrintType", style_str: str) -> None:
        if not isinstance(style_str, str):
            raise TypeError("style_str must be a string")
        self._styles[print_type] = style_str
