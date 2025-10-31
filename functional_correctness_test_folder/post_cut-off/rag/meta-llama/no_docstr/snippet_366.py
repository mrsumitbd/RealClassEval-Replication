
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    """Base configuration class with common CLI options."""
    config_dir: Path

    @property
    def khive_config_dir(self) -> Path:
        """Path to the .khive configuration directory."""
        return self.config_dir / '.khive'

    def update_from_cli_args(self, args: Any) -> None:
        """Update configuration from CLI arguments."""
        if hasattr(args, 'config_dir') and args.config_dir is not None:
            self.config_dir = Path(args.config_dir)
