
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:

    @property
    def khive_config_dir(self) -> Path:
        '''Path to the .khive configuration directory.'''
        return Path.home() / '.khive'

    def update_from_cli_args(self, args: Any) -> None:
        '''Update configuration from CLI arguments.'''
        for key, value in args.__dict__.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
