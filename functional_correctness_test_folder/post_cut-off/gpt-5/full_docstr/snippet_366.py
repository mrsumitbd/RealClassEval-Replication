from __future__ import annotations

import os
import sys
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Mapping


@dataclass
class BaseConfig:
    '''Base configuration class with common CLI options.'''

    @property
    def khive_config_dir(self) -> Path:
        '''Path to the .khive configuration directory.'''
        env_dir = os.environ.get("KHIVE_CONFIG_DIR")
        if env_dir:
            path = Path(os.path.expandvars(os.path.expanduser(env_dir)))
        else:
            if os.name == "nt" or sys.platform == "win32":
                base = os.environ.get("APPDATA") or os.environ.get(
                    "LOCALAPPDATA") or str(Path.home())
                path = Path(base) / "khive"
            else:
                xdg = os.environ.get("XDG_CONFIG_HOME")
                path = Path(xdg) / "khive" if xdg else Path.home() / ".khive"

        if path.exists() and not path.is_dir():
            raise NotADirectoryError(
                f"KHive config path exists and is not a directory: {path}")

        path.mkdir(parents=True, exist_ok=True)
        return path

    def update_from_cli_args(self, args: Any) -> None:
        '''Update configuration from CLI arguments.'''
        # Normalize args to a mapping-like object for lookup
        mapping: Mapping[str, Any]
        if isinstance(args, Mapping):
            mapping = args
        else:
            try:
                # works for argparse.Namespace and similar
                mapping = vars(args)
            except TypeError:
                # Fallback: wrap attribute access via getattr
                class _AttrMapping(dict):
                    def __missing__(self, key):
                        return getattr(args, key, None)
                mapping = _AttrMapping()

        for f in fields(self):
            name = f.name
            if name in mapping:
                value = mapping[name]
            else:
                value = getattr(args, name, None)

            if value is not None:
                setattr(self, name, value)
