
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    """Base configuration class with common CLI options."""
    khive_config_dir: Path

    @property
    def khive_config_dir(self) -> Path:
        """Path to the .khive configuration directory."""
        return self._khive_config_dir

    @khive_config_dir.setter
    def khive_config_dir(self, value: Path) -> None:
        self._khive_config_dir = value

    def update_from_cli_args(self, args: Any) -> None:
        """Update configuration from CLI arguments."""
        if hasattr(args, 'khive_config_dir') and args.khive_config_dir is not None:
            self.khive_config_dir = Path(args.khive_config_dir)
