
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    '''Base configuration class with common CLI options.'''

    # Optional attribute that subclasses may define
    config_dir: str | None = None

    @property
    def khive_config_dir(self) -> Path:
        '''Path to the .khive configuration directory.'''
        # If a custom config_dir is set, use it; otherwise default to ~/.khive
        if getattr(self, 'config_dir', None):
            return Path(self.config_dir).expanduser().resolve()
        return Path.home() / '.khive'

    def update_from_cli_args(self, args: Any) -> None:
        '''Update configuration from CLI arguments.'''
        # Iterate over all attributes in the argparse namespace
        for key, value in vars(args).items():
            # Skip None values to avoid overwriting defaults
            if value is None:
                continue
            # If the attribute exists on the config, update it
            if hasattr(self, key):
                setattr(self, key, value)
            # Special handling for config_dir to ensure Path resolution
            elif key == 'config_dir':
                self.config_dir = value
