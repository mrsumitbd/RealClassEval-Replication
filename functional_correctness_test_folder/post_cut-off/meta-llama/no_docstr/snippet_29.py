
import json
from pathlib import Path
from typing import Optional, Dict, Any


class Settings:
    # Assuming Settings class is defined elsewhere
    pass


class LastUsedParams:

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        if config_dir is None:
            self.config_dir = Path.home() / '.config'
        else:
            self.config_dir = config_dir
        self.config_file = self.config_dir / 'last_used_params.json'
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save(self, settings: 'Settings') -> None:
        data = settings.__dict__
        with open(self.config_file, 'w') as f:
            json.dump(data, f)

    def load(self) -> Dict[str, Any]:
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def clear(self) -> None:
        try:
            self.config_file.unlink()
        except FileNotFoundError:
            pass

    def exists(self) -> bool:
        return self.config_file.exists()
