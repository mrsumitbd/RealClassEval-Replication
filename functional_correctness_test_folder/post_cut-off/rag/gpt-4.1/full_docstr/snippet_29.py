from pathlib import Path
from typing import Optional, Dict, Any

import json


class LastUsedParams:
    '''Manages last used parameters persistence (moved from last_used.py).'''

    FILENAME = "last_used.json"

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        '''Initialize with config directory.'''
        if config_dir is None:
            self.config_dir = Path.home() / ".config" / "myapp"
        else:
            self.config_dir = config_dir
        self.filepath = self.config_dir / self.FILENAME
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save(self, settings: 'Settings') -> None:
        '''Save current settings as last used.'''
        data = settings.to_dict() if hasattr(settings, "to_dict") else dict(settings)
        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        if not self.filepath.exists():
            return {}
        with self.filepath.open("r", encoding="utf-8") as f:
            return json.load(f)

    def clear(self) -> None:
        '''Clear last used parameters.'''
        if self.filepath.exists():
            self.filepath.unlink()

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self.filepath.exists()
