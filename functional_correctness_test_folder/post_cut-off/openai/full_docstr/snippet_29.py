
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:
    """Manages last used parameters persistence (moved from last_used.py)."""

    _FILENAME = "last_used.json"

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """Initialize with config directory."""
        if config_dir is None:
            # Default to a hidden directory in the user's home
            config_dir = Path.home() / ".config" / "last_used_params"
        self.config_dir: Path = Path(config_dir).expanduser().resolve()
        self.file_path: Path = self.config_dir / self._FILENAME
        # Ensure the directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save(self, settings: "Settings") -> None:
        """Save current settings as last used."""
        # Try to get a serialisable representation of settings
        if hasattr(settings, "to_dict") and callable(settings.to_dict):
            data = settings.to_dict()
        else:
            # Fallback to the object's __dict__
            data = getattr(settings, "__dict__", {})
        # Ensure data is JSON serialisable
        try:
            json.dumps(data)
        except (TypeError, OverflowError) as exc:
            raise ValueError("Settings contain non-serialisable data") from exc
        # Write to file
        with self.file_path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2)

    def load(self) -> Dict[str, Any]:
        """Load last used parameters."""
        if not self.exists():
            return {}
        try:
            with self.file_path.open("r", encoding="utf-8") as fp:
                return json.load(fp)
        except (json.JSONDecodeError, OSError):
            # If the file is corrupted or unreadable, treat as empty
            return {}

    def clear(self) -> None:
        """Clear last used parameters."""
        if self.exists():
            try:
                self.file_path.unlink()
            except OSError:
                pass  # ignore errors on delete

    def exists(self) -> bool:
        """Check if last used params exist."""
        return self.file_path.is_file()
