import argparse
from typing import Any, Dict


class SearchAssistantConfig:
    def __init__(self, args: argparse.Namespace):
        if not isinstance(args, argparse.Namespace):
            raise TypeError("args must be an argparse.Namespace instance")
        self._data: Dict[str, Any] = dict(vars(args))
        reserved = set(dir(self.__class__)) | {"_data"}
        for key, value in self._data.items():
            if isinstance(key, str) and key.isidentifier() and key not in reserved and not key.startswith("_"):
                setattr(self, key, value)

    def validate(self) -> None:
        if not isinstance(self._data, dict):
            raise ValueError("Internal configuration storage is corrupted.")
        for key in self._data.keys():
            if not isinstance(key, str) or not key:
                raise ValueError(f"Invalid configuration key: {key!r}")
            if not key.isidentifier():
                raise ValueError(
                    f"Configuration key is not a valid identifier: {key!r}")
