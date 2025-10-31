
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    _khive_config_dir: Path = field(
        default_factory=lambda: Path.home() / ".khive")

    @property
    def khive_config_dir(self) -> Path:
        '''Path to the .khive configuration directory.'''
        return self._khive_config_dir

    def update_from_cli_args(self, args: Any) -> None:
        '''Update configuration from CLI arguments.'''
        if hasattr(args, 'khive_config_dir') and args.khive_config_dir is not None:
            self._khive_config_dir = Path(args.khive_config_dir)
