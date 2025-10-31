
from typing import Optional, Dict, Any
from pathlib import Path
import json


class LastUsedParams:

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        self.config_dir = config_dir or Path.home() / '.last_used_params'
        self.config_file = self.config_dir / 'params.json'
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save(self, settings: 'Settings') -> None:
        settings_dict = settings.to_dict()
        with open(self.config_file, 'w') as f:
            json.dump(settings_dict, f, indent=4)

    def load(self) -> Dict[str, Any]:
        if self.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

    def clear(self) -> None:
        if self.exists():
            self.config_file.unlink()

    def exists(self) -> bool:
        return self.config_file.exists()
