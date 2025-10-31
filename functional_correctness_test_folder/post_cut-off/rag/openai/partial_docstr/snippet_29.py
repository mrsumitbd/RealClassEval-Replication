
import json
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:
    '''Manages last used parameters persistence (moved from last_used.py).'''

    _FILENAME = "last_used.json"

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        '''Initialize with config directory.'''
        if config_dir is None:
            # Default to a hidden directory in the user's home
            config_dir = Path.home() / ".config" / "pyvlx"
        self.config_dir = Path(config_dir).expanduser().resolve()
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.config_dir / self._FILENAME

    def save(self, settings: "Settings") -> None:
        '''Save current settings as last used.'''
        # Try to get a serialisable dict from settings
        if hasattr(settings, "to_dict") and callable(settings.to_dict):
            data = settings.to_dict()
        else:
            # Fallback to the instance __dict__
            data = {k: v for k, v in settings.__dict__.items()
                    if not k.startswith("_")}
        # Write JSON to file
        with self.file_path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=4, sort_keys=True)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        if not self.file_path.is_file():
            return {}
        try:
            with self.file_path.open("r", encoding="utf-8") as fp:
                return json.load(fp)
        except (json.JSONDecodeError, OSError):
            # If file is corrupted or unreadable, treat as empty
            return {}

    def clear(self) -> None:
        '''Clear last used parameters.'''
        if self.file_path.is_file():
            try:
                self.file_path.unlink()
            except OSError:
                pass

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self.file_path.is_file()
