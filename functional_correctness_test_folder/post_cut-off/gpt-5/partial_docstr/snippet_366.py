from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Mapping
import os


@dataclass
class BaseConfig:

    @property
    def khive_config_dir(self) -> Path:
        '''Path to the .khive configuration directory.'''
        env = os.getenv("KHIVE_CONFIG_DIR")
        return Path(env).expanduser() if env else Path.home() / ".khive"

    def update_from_cli_args(self, args: Any) -> None:
        '''Update configuration from CLI arguments.'''
        def get_arg_value(name: str) -> Any:
            if isinstance(args, Mapping):
                if name in args:
                    return args[name]
                dashed = name.replace("_", "-")
                if dashed in args:
                    return args[dashed]
                return None
            if hasattr(args, name):
                return getattr(args, name)
            dashed = name.replace("_", "-")
            if hasattr(args, dashed):
                return getattr(args, dashed)
            return None

        for f in fields(self):
            val = get_arg_value(f.name)
            if val is not None:
                setattr(self, f.name, val)
