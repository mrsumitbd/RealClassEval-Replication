
import json
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:
    '''Manages last used parameters persistence (moved from last_used.py).'''

    _FILENAME = "last_used.json"

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        '''Initialize with config directory.'''
        if config_dir is None:
            config_dir = Path.home() / ".config" / "myapp"
        self.config_dir = Path(config_dir)
        self.file_path = self.config_dir / self._FILENAME
        # Ensure directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save(self, settings: "Settings") -> None:
        '''Save current settings as last used.'''
        # Convert settings to a serialisable dict
        if hasattr(settings, "__dict__"):
            data = dict(settings.__dict__)
        else:
            # Fallback: try to get attributes via dir
            data = {k: getattr(settings, k) for k in dir(settings)
                    if not k.startswith("_") and not callable(getattr(settings, k))}
        # Write JSON
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        if not self.file_path.exists():
            return {}
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # If file is corrupted or unreadable, treat as empty
            return {}

    def clear(self) -> None:
        '''Clear last used parameters.'''
        if self.file_path.exists():
            try:
                self.file_path.unlink()
            except Exception:
                pass

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self.file_path.exists()
