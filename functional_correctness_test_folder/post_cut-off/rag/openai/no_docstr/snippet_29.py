
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
        self.config_dir = Path(config_dir)
        self.file_path = self.config_dir / self._FILENAME

    def save(self, settings: "Settings") -> None:
        '''Save current settings as last used.'''
        # Ensure the config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Convert settings to a serialisable dict
        if hasattr(settings, "to_dict") and callable(settings.to_dict):
            data = settings.to_dict()
        else:
            # Fallback: use the instance's __dict__
            data = dict(settings.__dict__)

        # Write JSON to file
        with self.file_path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2, sort_keys=True)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        if not self.file_path.exists():
            return {}
        try:
            with self.file_path.open("r", encoding="utf-8") as fp:
                return json.load(fp)
        except Exception:
            # If the file is corrupted or unreadable, treat as empty
            return {}

    def clear(self) -> None:
        '''Clear last used parameters.'''
        if self.file_path.exists():
            try:
                self.file_path.unlink()
            except Exception:
                pass

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self.file_path.exists()
