
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    '''Base configuration class with common CLI options.'''
    config_dir: Path = Path.home() / '.khive'

    @property
    def khive_config_dir(self) -> Path:
        '''Path to the .khive configuration directory.'''
        return self.config_dir

    def update_from_cli_args(self, args: Any) -> None:
        '''Update configuration from CLI arguments.'''
        if hasattr(args, 'config_dir') and args.config_dir:
            self.config_dir = Path(args.config_dir)
