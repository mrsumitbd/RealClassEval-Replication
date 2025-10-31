
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field


@dataclass
class BaseConfig:
    """Base configuration class with common CLI options."""

    # Internal storage for the configuration directory.
    _khive_config_dir: Path = field(
        default_factory=lambda: Path.home() / ".khive")

    @property
    def khive_config_dir(self) -> Path:
        """Path to the .khive configuration directory."""
        return self._khive_config_dir

    def update_from_cli_args(self, args: Any) -> None:
        """Update configuration from CLI arguments.

        Parameters
        ----------
        args : Any
            Namespace or object containing CLI arguments.  Only attributes
            that already exist on the instance are updated.  ``None`` values
            are ignored.
        """
        # Allow overriding the config directory via CLI.
        if hasattr(args, "khive_config_dir") and args.khive_config_dir is not None:
            self._khive_config_dir = Path(args.khive_config_dir)

        # Update any other attributes that exist on the instance.
        for key, value in vars(args).items():
            if value is None:
                continue
            if hasattr(self, key):
                setattr(self, key, value)
