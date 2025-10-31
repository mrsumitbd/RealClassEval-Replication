
from typing import Optional, Dict, Any
from pathlib import Path
import json


class LastUsedParams:

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        if config_dir is None:
            self.config_dir = Path.home() / ".last_used_params"
        else:
            self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.config_dir / "last_used_params.json"

    def save(self, settings: 'Settings') -> None:
        # Assume settings has a .dict() method or is dict-like
        if hasattr(settings, "dict"):
            data = settings.dict()
        elif hasattr(settings, "__dict__"):
            data = dict(settings.__dict__)
        else:
            data = dict(settings)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> Dict[str, Any]:
        if not self.file_path.exists():
            return {}
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def clear(self) -> None:
        if self.file_path.exists():
            self.file_path.unlink()

    def exists(self) -> bool:
        return self.file_path.exists()
