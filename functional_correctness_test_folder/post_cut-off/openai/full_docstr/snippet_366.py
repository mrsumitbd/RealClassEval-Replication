
from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    '''Base configuration class with common CLI options.'''

    @property
    def khive_config_dir(self) -> Path:
        '''Path to the .khive configuration directory.'''
        return Path.home() / ".khive"

    def update_from_cli_args(self, args: Any) -> None:
        '''Update configuration from CLI arguments.'''
        # Iterate over all dataclass fields and update if the attribute exists in args
        for f in fields(self):
            if hasattr(args, f.name):
                setattr(self, f.name, getattr(args, f.name))
