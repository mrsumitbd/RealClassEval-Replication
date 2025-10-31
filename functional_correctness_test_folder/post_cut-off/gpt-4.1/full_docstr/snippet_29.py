
from typing import Optional, Dict, Any
from pathlib import Path
import json


class LastUsedParams:
    '''Manages last used parameters persistence (moved from last_used.py).'''

    FILENAME = "last_used_params.json"

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        '''Initialize with config directory.'''
        if config_dir is None:
            self.config_dir = Path.home() / ".config" / "last_used_params"
        else:
            self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.config_dir / self.FILENAME

    def save(self, settings: 'Settings') -> None:
        '''Save current settings as last used.'''
        # Assume settings has a .to_dict() method
        data = settings.to_dict() if hasattr(settings, "to_dict") else dict(settings)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        if not self.filepath.exists():
            return {}
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def clear(self) -> None:
        '''Clear last used parameters.'''
        if self.filepath.exists():
            self.filepath.unlink()

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self.filepath.exists()
