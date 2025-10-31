
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    config_dir: Path

    @property
    def khive_config_dir(self) -> Path:
        return self.config_dir / 'khive'

    def update_from_cli_args(self, args: Any) -> None:
        if hasattr(args, 'config_dir'):
            self.config_dir = Path(args.config_dir)
