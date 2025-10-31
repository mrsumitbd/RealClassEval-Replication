from __future__ import annotations

import json
import os
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:
    '''Manages last used parameters persistence (moved from last_used.py).'''

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        '''Initialize with config directory.'''
        if config_dir is None:
            config_dir = Path.home() / ".config"
        self._config_dir = Path(config_dir)
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._file = self._config_dir / "last_used_params.json"

    def _to_mapping(self, settings: Any) -> Dict[str, Any]:
        if isinstance(settings, dict):
            return dict(settings)
        if hasattr(settings, "to_dict") and callable(getattr(settings, "to_dict")):
            try:
                return dict(settings.to_dict())
            except Exception:
                pass
        if is_dataclass(settings):
            try:
                return asdict(settings)
            except Exception:
                pass
        if hasattr(settings, "__iter__") and not hasattr(settings, "__dict__"):
            try:
                return dict(settings)  # type: ignore[arg-type]
            except Exception:
                pass
        if hasattr(settings, "__dict__"):
            return dict(vars(settings))
        raise TypeError(
            "Unsupported settings type; expected dict-like, dataclass, or object with to_dict/attributes.")

    def _jsonify(self, value: Any) -> Any:
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, Enum):
            return value.value  # type: ignore[return-value]
        if isinstance(value, bytes):
            try:
                return value.decode("utf-8")
            except Exception:
                return value.hex()
        if isinstance(value, (set, tuple)):
            return [self._jsonify(v) for v in value]
        if isinstance(value, list):
            return [self._jsonify(v) for v in value]
        if isinstance(value, dict):
            return {str(k): self._jsonify(v) for k, v in value.items()}
        try:
            json.dumps(value)
            return value
        except Exception:
            return str(value)

    def save(self, settings: 'Settings') -> None:
        '''Save current settings as last used.'''
        data = self._to_mapping(settings)
        serializable = self._jsonify(data)
        tmp_path = self._file.with_suffix(".json.tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self._file)

    def load(self) -> Dict[str, Any]:
        '''Load last used parameters.'''
        if not self._file.exists():
            return {}
        try:
            with self._file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            return {}

    def clear(self) -> None:
        '''Clear last used parameters.'''
        try:
            if self._file.exists():
                self._file.unlink()
        except Exception:
            pass

    def exists(self) -> bool:
        '''Check if last used params exist.'''
        return self._file.exists()
