
from pathlib import Path
from typing import Any, Dict, Optional, Union
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
        settings_dict = settings.to_dict()  # Assuming Settings has a method to_dict()
        with self.config_file.open('w') as f:
            json.dump(settings_dict, f, indent=4)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        if not self.exists():
            return {}
        with self.config_file.open('r') as f:
            return json.load(f)

    def clear(self) -> None:
        '''Clear last used parameters.'''
        if self.exists():
            self.config_file.unlink()

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self.config_file.exists()
