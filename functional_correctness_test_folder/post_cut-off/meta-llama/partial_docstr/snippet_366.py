
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    def __post_init__(self):
        self._khive_config_dir = None

    @property
    def khive_config_dir(self) -> Path:
        '''Path to the .khive configuration directory.'''
        if self._khive_config_dir is None:
            self._khive_config_dir = Path.home() / '.khive'
        return self._khive_config_dir

    def update_from_cli_args(self, args: Any) -> None:
        '''Update configuration from CLI arguments.'''
        if hasattr(args, 'khive_config_dir'):
            self._khive_config_dir = Path(args.khive_config_dir)
