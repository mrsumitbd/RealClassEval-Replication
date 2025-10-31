from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Mapping, Optional, Union, get_args, get_origin
import os


@dataclass
class BaseConfig:
    """Base configuration class with common CLI options."""
    config_dir: Optional[Path] = None

    @property
    def khive_config_dir(self) -> Path:
        """Path to the .khive configuration directory."""
        env = os.getenv("KHIVE_CONFIG_DIR")
        if self.config_dir is not None:
            return Path(self.config_dir).expanduser().resolve()
        if env:
            return Path(env).expanduser().resolve()
        return (Path.home() / ".khive").resolve()

    def update_from_cli_args(self, args: Any) -> None:
        """Update configuration from CLI arguments."""
        if isinstance(args, Mapping):
            data = dict(args)
        else:
            try:
                data = dict(vars(args))
            except TypeError:
                data = {}

        for f in fields(self):
            name = f.name
            if name not in data:
                continue
            value = data[name]
            if value is None:
                continue

            typ = f.type
            coerce_to_path = False
            if typ is Path:
                coerce_to_path = True
            else:
                origin = get_origin(typ)
                if origin is Union and Path in get_args(typ):
                    coerce_to_path = True

            if coerce_to_path and not isinstance(value, Path):
                value = Path(value)

            setattr(self, name, value)
