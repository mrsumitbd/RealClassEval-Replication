
import json
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:
    """Manages last used parameters persistence (moved from last_used.py)."""

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """Initialize with config directory."""
        self.config_dir = config_dir or Path.home() / '.config'
        self.last_used_file = self.config_dir / 'last_used.json'

    def save(self, settings: 'Settings') -> None:
        """Save current settings as last used."""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        with open(self.last_used_file, 'w') as file:
            json.dump(settings.__dict__, file)

    def load(self) -> Dict[str, Any]:
        """Load last used parameters."""
        try:
            with open(self.last_used_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def clear(self) -> None:
        """Clear last used parameters."""
        try:
            self.last_used_file.unlink()
        except FileNotFoundError:
            pass

    def exists(self) -> bool:
        """Check if last used params exist."""
        return self.last_used_file.exists()
