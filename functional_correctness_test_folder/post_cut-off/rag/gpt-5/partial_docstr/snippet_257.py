from typing import Dict, Optional
import os
import json
from pathlib import Path

try:
    import yaml  # type: ignore
    _HAVE_YAML = True
except Exception:
    _HAVE_YAML = False


class TerminalTextStyles:
    '''Manages loading, saving, and applying terminal text styles.'''

    def __init__(self, stylesheet_path: str = None):
        '''
            Initializes the style manager.
            Args:
                stylesheet_path: Optional path to the stylesheet. Defaults to
                                 a file in the JRDEV_DIR.
        '''
        if stylesheet_path is None:
            jrdev_dir = os.environ.get(
                "JRDEV_DIR", str(Path.home() / ".jrdev"))
            stylesheet_path = str(Path(jrdev_dir) / "terminal_styles.json")
        self._stylesheet_path: str = stylesheet_path
        self._styles: Dict[str, str] = {}
        self.load_styles()

    def _get_default_styles(self) -> Dict[str, str]:
        '''Returns the default styles for each PrintType as a dictionary.'''
        defaults = {
            "INFO": "\033[37m",        # White
            "SUCCESS": "\033[32m",     # Green
            "WARNING": "\033[33m",     # Yellow
            "ERROR": "\033[31m",       # Red
            "DEBUG": "\033[36m",       # Cyan
            "PROMPT": "\033[1;34m",    # Bold Blue
            "TITLE": "\033[1;97m",     # Bold Bright White
        }
        return defaults

    def load_styles(self) -> None:
        '''Loads styles from the stylesheet file, merging them with defaults.'''
        defaults = self._get_default_styles()
        path = Path(self._stylesheet_path)

        if not path.exists():
            self._styles = defaults
            return

        loaded: Dict[str, str] = {}
        try:
            text = path.read_text(encoding="utf-8")
            if path.suffix.lower() in (".yaml", ".yml"):
                if not _HAVE_YAML:
                    raise RuntimeError(
                        "PyYAML not available to parse YAML stylesheet.")
                data = yaml.safe_load(text) or {}
            else:
                # Default to JSON, try JSON first; if it fails and YAML available, try YAML
                try:
                    data = json.loads(text)
                except Exception:
                    if _HAVE_YAML:
                        data = yaml.safe_load(text) or {}
                    else:
                        raise
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(k, str) and isinstance(v, str):
                        loaded[k.upper()] = v
        except Exception:
            # On any error, fall back to defaults
            loaded = {}

        merged = defaults.copy()
        merged.update(loaded)
        self._styles = merged

    def save_styles(self) -> bool:
        '''Saves the current styles to the stylesheet file.'''
        try:
            path = Path(self._stylesheet_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix.lower() in (".yaml", ".yml"):
                if not _HAVE_YAML:
                    # If YAML requested but unavailable, write JSON alongside
                    path = path.with_suffix(".json")
                    path.write_text(json.dumps(
                        self._styles, indent=2, ensure_ascii=False), encoding="utf-8")
                else:
                    path.write_text(
                        # type: ignore
                        yaml.safe_dump(self._styles, sort_keys=True),
                        encoding="utf-8",
                    )
            else:
                path.write_text(json.dumps(self._styles, indent=2,
                                ensure_ascii=False), encoding="utf-8")
            return True
        except Exception:
            return False

    def get_style(self, print_type: 'PrintType') -> str:
        '''Gets the style string for a given PrintType.'''
        key = getattr(print_type, "name", str(print_type))
        return self._styles.get(str(key).upper(), "")

    def set_style(self, print_type: 'PrintType', style_str: str) -> None:
        '''Sets the style for a given PrintType.'''
        if not isinstance(style_str, str):
            raise TypeError("style_str must be a string")
        key = getattr(print_type, "name", str(print_type))
        self._styles[str(key).upper()] = style_str
