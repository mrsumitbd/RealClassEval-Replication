
from pathlib import Path
from typing import Optional, Dict, Any
import json
import os


class LastUsedParams:

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        self.config_dir = config_dir if config_dir is not None else Path.home() / \
            ".config"
        self.file_path = self.config_dir / "last_used_params.json"

    def save(self, settings: 'Settings') -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w') as f:
            json.dump(settings.__dict__, f)

    def load(self) -> Dict[str, Any]:
        if not self.exists():
            return {}
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def clear(self) -> None:
        if self.exists():
            os.remove(self.file_path)

    def exists(self) -> bool:
        return self.file_path.exists()
