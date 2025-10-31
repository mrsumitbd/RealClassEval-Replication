
import json
from pathlib import Path
from typing import Optional, Dict, Any


class LastUsedParams:
    '''Manages last used parameters persistence (moved from last_used.py).'''

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        '''Initialize with config directory.'''
        self.config_dir = config_dir or Path.home() / '.config'
        self.last_used_file = self.config_dir / 'last_used_params.json'

    def save(self, settings: 'Settings') -> None:
        '''Save current settings as last used.'''
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.last_used_file, 'w') as f:
            json.dump(settings.__dict__, f)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        if not self.exists():
            return {}
        with open(self.last_used_file, 'r') as f:
            return json.load(f)

    def clear(self) -> None:
        '''Clear last used parameters.'''
        if self.exists():
            self.last_used_file.unlink()

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self.last_used_file.exists()
