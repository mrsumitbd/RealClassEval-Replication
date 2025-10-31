from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:
    _FILENAME = "last_used_params.json"

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        if config_dir is None:
            self._path = Path.home() / f".{self._FILENAME}"
        else:
            self._path = Path(config_dir) / self._FILENAME
            self._path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, settings: 'Settings') -> None:
        data = self._coerce_to_dict(settings)
        sanitized = self._sanitize_for_json(data)
        self._path.write_text(json.dumps(
            sanitized, indent=2, sort_keys=True), encoding="utf-8")

    def load(self) -> Dict[str, Any]:
        if not self._path.exists():
            return {}
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def clear(self) -> None:
        try:
            if self._path.exists():
                self._path.unlink()
        except OSError:
            pass

    def exists(self) -> bool:
        return self._path.exists()

    @staticmethod
    def _coerce_to_dict(settings: Any) -> Dict[str, Any]:
        if settings is None:
            return {}
        if isinstance(settings, dict):
            return dict(settings)
        if is_dataclass(settings):
            return asdict(settings)
        to_dict = getattr(settings, "to_dict", None)
        if callable(to_dict):
            return dict(to_dict())
        model_dump = getattr(settings, "model_dump", None)
        if callable(model_dump):
            return dict(model_dump())
        dunder_dict = getattr(settings, "__dict__", None)
        if isinstance(dunder_dict, dict):
            return dict(dunder_dict)
        raise TypeError("Unsupported Settings object: cannot coerce to dict")

    @classmethod
    def _sanitize_for_json(cls, value: Any) -> Any:
        try:
            json.dumps(value)
            return value
        except TypeError:
            pass

        if isinstance(value, dict):
            return {str(k): cls._sanitize_for_json(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [cls._sanitize_for_json(v) for v in value]
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return repr(value)
