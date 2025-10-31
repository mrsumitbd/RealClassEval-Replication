
import json
from pathlib import Path
from typing import Optional, Dict, Any


class LastUsedParams:

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        self.config_dir = config_dir or Path.home() / ".config" / "last_used_params"
        self.config_file = self.config_dir / "last_used_params.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save(self, settings: 'Settings') -> None:
        with open(self.config_file, 'w') as f:
            json.dump(settings.__dict__, f)

    def load(self) -> Dict[str, Any]:
        if not self.exists():
            return {}
        with open(self.config_file, 'r') as f:
            return json.load(f)

    def clear(self) -> None:
        if self.exists():
            self.config_file.unlink()

    def exists(self) -> bool:
        return self.config_file.exists()
