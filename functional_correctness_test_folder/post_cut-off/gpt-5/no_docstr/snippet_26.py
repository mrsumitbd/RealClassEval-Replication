from typing import Any, Dict, Iterable, Mapping
from dataclasses import is_dataclass, asdict
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from uuid import UUID
from pathlib import Path
import base64


class DataConverter:

    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        flat: Dict[str, Any] = {}

        def _flatten(obj: Any, current_prefix: str) -> None:
            if isinstance(obj, Mapping):
                for k, v in obj.items():
                    key = f"{current_prefix}.{k}" if current_prefix else str(k)
                    _flatten(v, key)
            elif isinstance(obj, (list, tuple)):
                for i, v in enumerate(obj):
                    key = f"{current_prefix}.{i}" if current_prefix else str(i)
                    _flatten(v, key)
            else:
                flat[current_prefix] = obj

        _flatten(data, prefix if prefix else '')
        return flat

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        target_keys = {'model', 'model_name', 'modelName'}

        def _search(obj: Any) -> str | None:
            if isinstance(obj, Mapping):
                for k, v in obj.items():
                    if str(k) in target_keys and isinstance(v, str) and v.strip():
                        return v
                    res = _search(v)
                    if res:
                        return res
            elif isinstance(obj, (list, tuple)):
                for item in obj:
                    res = _search(item)
                    if res:
                        return res
            return None

        found = _search(data)
        return found if found else default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        # Primitives
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj

        # datetime, date, time
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()

        # Decimal
        if isinstance(obj, Decimal):
            # Use string to avoid float precision issues
            return str(obj)

        # Enum
        if isinstance(obj, Enum):
            val = obj.value
            return DataConverter.to_serializable(val)

        # UUID, Path
        if isinstance(obj, (UUID, Path)):
            return str(obj)

        # bytes/bytearray
        if isinstance(obj, (bytes, bytearray)):
            return base64.b64encode(obj).decode('ascii')

        # Dataclass
        if is_dataclass(obj):
            return DataConverter.to_serializable(asdict(obj))

        # Objects that provide to_dict()/dict()/model_dump()
        for attr in ('to_dict', 'dict', 'model_dump'):
            if hasattr(obj, attr) and callable(getattr(obj, attr)):
                try:
                    d = getattr(obj, attr)()
                    return DataConverter.to_serializable(d)
                except Exception:
                    pass

        # Numpy-like arrays / pandas objects with tolist()
        if hasattr(obj, 'tolist') and callable(getattr(obj, 'tolist')):
            try:
                return DataConverter.to_serializable(obj.tolist())
            except Exception:
                pass

        # Mapping
        if isinstance(obj, Mapping):
            return {str(k): DataConverter.to_serializable(v) for k, v in obj.items()}

        # Iterable (but not string/bytes handled earlier)
        if isinstance(obj, Iterable):
            try:
                return [DataConverter.to_serializable(x) for x in obj]
            except Exception:
                pass

        # Fallback to __dict__ if available
        if hasattr(obj, '__dict__'):
            try:
                return DataConverter.to_serializable(vars(obj))
            except Exception:
                pass

        # Final fallback: string representation
        return str(obj)
