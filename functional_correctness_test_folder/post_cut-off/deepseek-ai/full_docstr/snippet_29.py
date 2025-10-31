
import json
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:
    '''Manages last used parameters persistence (moved from last_used.py).'''

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        '''Initialize with config directory.'''
        self._config_dir = config_dir or Path.home() / ".config"
        self._file_path = self._config_dir / "last_used_params.json"

    def save(self, settings: 'Settings') -> None:
        '''Save current settings as last used.'''
        self._config_dir.mkdir(parents=True, exist_ok=True)
        with open(self._file_path, "w") as f:
            json.dump(settings.__dict__, f)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        try:
            with open(self._file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def clear(self) -> None:
        '''Clear last used parameters.'''
        try:
            self._file_path.unlink()
        except FileNotFoundError:
            pass

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self._file_path.exists()
