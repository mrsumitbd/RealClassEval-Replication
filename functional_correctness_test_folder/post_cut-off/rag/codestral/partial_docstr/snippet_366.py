
from pathlib import Path
from typing import Any
from dataclasses import dataclass


@dataclass
class BaseConfig:
    '''Base configuration class with common CLI options.'''
    @property
    def khive_config_dir(self) -> Path:
        '''Path to the .khive configuration directory.'''
        return Path.home() / '.khive'

    def update_from_cli_args(self, args: Any) -> None:
        '''Update configuration from CLI arguments.'''
        for key, value in vars(args).items():
            if hasattr(self, key):
                setattr(self, key, value)
