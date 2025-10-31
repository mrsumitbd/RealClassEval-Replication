
from typing import Optional, Dict, Any
from pathlib import Path
import json


class LastUsedParams:
    '''Manages last used parameters persistence (moved from last_used.py).'''

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        '''Initialize with config directory.'''
        self.config_dir = config_dir or Path.home() / '.config' / 'app_name'
        self.config_file = self.config_dir / 'last_used_params.json'
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save(self, settings: 'Settings') -> None:
        '''Save current settings as last used.'''
        with self.config_file.open('w') as f:
            json.dump(settings.to_dict(), f)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        if self.exists():
            with self.config_file.open('r') as f:
                return json.load(f)
        return {}

    def clear(self) -> None:
        '''Clear last used parameters.'''
        if self.exists():
            self.config_file.unlink()

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self.config_file.exists()
