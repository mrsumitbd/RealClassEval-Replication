from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional
import dataclasses
from enum import Enum
from datetime import date, datetime
from types import MappingProxyType


class LastUsedParams:
    def __init__(self, config_dir: Optional[Path] = None) -> None:
        if config_dir is None:
            config_dir = Path.home() / ".last_used_params"
        self._dir = Path(config_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._file = self._dir / "last_used.json"

    def save(self, settings: 'Settings') -> None:
        data = self._extract_settings(settings)
        jsonable = self._make_jsonable(data)
        self._dir.mkdir(parents=True, exist_ok=True)
        tmp_file = self._file.with_suffix(".json.tmp")
        with tmp_file.open("w", encoding="utf-8") as f:
            json.dump(jsonable, f, ensure_ascii=False,
                      indent=2, sort_keys=True)
        tmp_file.replace(self._file)

    def load(self) -> Dict[str, Any]:
        if not self.exists():
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
        try:
            if self._file.exists():
                self._file.unlink()
        except Exception:
            pass

    def exists(self) -> bool:
        return self._file.exists()

    def _extract_settings(self, settings: Any) -> Dict[str, Any]:
        # Pydantic v2
        for attr in ("model_dump",):
            fn = getattr(settings, attr, None)
            if callable(fn):
                try:
                    return fn()  # type: ignore[call-arg]
                except Exception:
                    pass
        # Pydantic v1
        for attr in ("dict",):
            fn = getattr(settings, attr, None)
            if callable(fn):
                try:
                    return fn()  # type: ignore[call-arg]
                except Exception:
                    pass
        # Generic to_dict / as_dict
        for attr in ("to_dict", "as_dict"):
            fn = getattr(settings, attr, None)
            if callable(fn):
                try:
                    return fn()  # type: ignore[call-arg]
                except Exception:
                    pass
        # Dataclasses
        if dataclasses.is_dataclass(settings):
            try:
                return dataclasses.asdict(settings)
            except Exception:
                pass
        # Fallback to __dict__
        try:
            return {
                k: v
                for k, v in vars(settings).items()
                if not callable(v) and not k.startswith("_")
            }
        except Exception:
            return {}

    def _make_jsonable(self, obj: Any) -> Any:
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Path):
            return str(obj)
        if isinstance(obj, Enum):
            return obj.value if not isinstance(obj.value, (Enum,)) else obj.name
        if isinstance(obj, MappingProxyType):
            obj = dict(obj)
        if isinstance(obj, dict):
            return {str(self._make_jsonable(k)): self._make_jsonable(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple, set)):
            return [self._make_jsonable(v) for v in obj]
        # Objects with __dict__
        if hasattr(obj, "__dict__"):
            try:
                return self._make_jsonable(
                    {k: v for k, v in vars(obj).items() if not callable(
                        v) and not k.startswith("_")}
                )
            except Exception:
                pass
        # Fallback to string
        try:
            return str(obj)
        except Exception:
            return None
