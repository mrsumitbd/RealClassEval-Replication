
import json
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        self.config_dir = config_dir or Path.home() / ".config"
        self.file_path = self.config_dir / "last_used_params.json"
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, settings: 'Settings') -> None:
        with open(self.file_path, 'w') as f:
            json.dump(settings.__dict__, f)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def clear(self) -> None:
        if self.file_path.exists():
            self.file_path.unlink()

    def exists(self) -> bool:
        return self.file_path.exists()
