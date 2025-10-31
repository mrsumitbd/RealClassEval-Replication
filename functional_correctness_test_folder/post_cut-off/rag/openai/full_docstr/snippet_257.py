
import os
import yaml
from pathlib import Path
from typing import Dict, Any

# The PrintType enum is expected to be defined elsewhere in the project.
# Import it here; if it is not available, the code will still work
# with any hashable key (e.g. strings) but the type hint will be
# a fallback to `Any`.
try:
    from .print_types import PrintType  # type: ignore
except Exception:  # pragma: no cover
    from typing import Any as PrintType  # type: ignore


class TerminalTextStyles:
    """Manages loading, saving, and applying terminal text styles."""

    def __init__(self, stylesheet_path: str | None = None) -> None:
        """
        Initializes the style manager.

        Args:
            stylesheet_path: Optional path to the stylesheet. Defaults to
                             a file in the JRDEV_DIR.
        """
        # Determine the default stylesheet location
        if stylesheet_path is None:
            jrdev_dir = os.getenv("JRDEV_DIR", ".")
            stylesheet_path = Path(jrdev_dir) / "terminal_styles.yml"
        self.stylesheet_path = Path(stylesheet_path).expanduser().resolve()

        # Ensure the directory exists
        self.stylesheet_path.parent.mkdir(parents=True, exist_ok=True)

        # Load styles (will merge defaults)
        self.styles: Dict[Any, str] = {}
        self.load_styles()

    def _get_default_styles(self) -> Dict[Any, str]:
        """Returns the default styles for each PrintType as a dictionary."""
        # ANSI escape codes for common colors
        defaults: Dict[Any, str] = {
            "INFO": "\033[32m",      # green
            "WARNING": "\033[33m",   # yellow
            "ERROR": "\033[31m",     # red
            "DEBUG": "\033[34m",     # blue
            "RESET": "\033[0m",      # reset
        }
        return defaults

    def load_styles(self) -> None:
        """Loads styles from the stylesheet file, merging them with defaults."""
        defaults = self._get_default_styles()
        self.styles = defaults.copy()

        if self.stylesheet_path.is_file():
            try:
                with self.stylesheet_path.open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                if isinstance(data, dict):
                    # Merge user styles over defaults
                    for key, value in data.items():
                        self.styles[key] = value
            except Exception as exc:  # pragma: no cover
                # If loading fails, keep defaults and log the error
                print(
                    f"Warning: could not load styles from {self.stylesheet_path}: {exc}")

    def save_styles(self) -> bool:
        """Saves the current styles to the stylesheet file."""
        try:
            with self.stylesheet_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(self.styles, f, default_flow_style=False)
            return True
        except Exception as exc:  # pragma: no cover
            print(
                f"Error: could not save styles to {self.stylesheet_path}: {exc}")
            return False

    def get_style(self, print_type: Any) -> str:
        """Gets the style string for a given PrintType."""
        return self.styles.get(str(print_type), "")

    def set_style(self, print_type: Any, style_str: str) -> None:
        """Sets the style for a given PrintType."""
        self.styles[str(print_type)] = style_str
