
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    """Base configuration class with common CLI options."""

    # Default configuration directory (can be overridden by CLI args)
    config_dir: Path | None = None

    @property
    def khive_config_dir(self) -> Path:
        """Path to the .khive configuration directory."""
        # If config_dir is not set, default to ~/.khive
        return self.config_dir or Path.home() / ".khive"

    def update_from_cli_args(self, args: Any) -> None:
        """Update configuration from CLI arguments.

        Parameters
        ----------
        args : Any
            Namespace or object returned by an argument parser.  Only
            attributes that already exist on ``self`` are updated.
        """
        # Iterate over all attributes of the args object
        for key, value in vars(args).items():
            # Skip private or special attributes
            if key.startswith("_"):
                continue
            # Only update if the attribute exists on the config instance
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
