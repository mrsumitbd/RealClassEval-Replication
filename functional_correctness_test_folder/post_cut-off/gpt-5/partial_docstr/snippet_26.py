from typing import Any, Dict, Iterable
import dataclasses as _dc
import datetime as _dt
import decimal as _decimal
import uuid as _uuid
import pathlib as _pathlib
import enum as _enum
import inspect as _inspect
from collections.abc import Mapping as _Mapping

try:
    import numpy as _np  # type: ignore
except Exception:
    _np = None

try:
    import pandas as _pd  # type: ignore
except Exception:
    _pd = None


class DataConverter:
    '''Unified data conversion utilities.'''
    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        result: Dict[str, Any] = {}

        def _flatten(obj: Any, current_prefix: str) -> None:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    key = f"{current_prefix}.{k}" if current_prefix else str(k)
                    _flatten(v, key)
            elif isinstance(obj, (list, tuple)):
                for i, item in enumerate(obj):
                    key = f"{current_prefix}.{i}" if current_prefix else str(i)
                    _flatten(item, key)
            else:
                result[current_prefix] = obj

        _flatten(data, prefix if prefix else '')
        return result

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        def _is_model_like(val: Any) -> bool:
            return isinstance(val, str) and len(val.strip()) > 0

        priority_keys = [
            'model',
            'model_name',
            'modelId',
            'model_id',
            'modelSlug',
            'deployment',
            'deployment_name',
            'engine',
            'name',
            'llm',
            'gpt_model',
        ]

        # Direct top-level checks first
        for k in priority_keys:
            if k in data and _is_model_like(data[k]):
                return str(data[k]).strip()

        flat = DataConverter.flatten_nested_dict(data)

        # Priority exact matches on flattened keys (end segment)
        for k in priority_keys:
            for fk, fv in flat.items():
                if fk.endswith(f".{k}") or fk == k:
                    if _is_model_like(fv):
                        return str(fv).strip()

        # Heuristic search: any key containing 'model'
        for fk, fv in flat.items():
            low = fk.lower()
            if 'model' in low and _is_model_like(fv):
                return str(fv).strip()

        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        def _convert(o: Any, seen: set[int]) -> Any:
            if o is None or isinstance(o, (bool, int, float, str)):
                return o

            oid = id(o)
            if oid in seen:
                return f"<circular_ref:{type(o).__name__}>"
            seen.add(oid)

            if isinstance(o, (bytes, bytearray, memoryview)):
                try:
                    return bytes(o).decode('utf-8', errors='replace')
                except Exception:
                    return str(o)

            if isinstance(o, (_dt.datetime, _dt.date, _dt.time)):
                try:
                    return o.isoformat()
                except Exception:
                    return str(o)

            if isinstance(o, _dt.timedelta):
                return o.total_seconds()

            if isinstance(o, _uuid.UUID):
                return str(o)

            if isinstance(o, _decimal.Decimal):
                return str(o)

            if isinstance(o, (_pathlib.Path, )):
                return str(o)

            if isinstance(o, (_enum.Enum, )):
                val = o.value
                try:
                    return _convert(val, seen)
                except Exception:
                    return str(val)

            if _dc.is_dataclass(o):
                try:
                    return _convert(_dc.asdict(o), seen)
                except Exception:
                    return str(o)

            if _np is not None:
                if isinstance(o, getattr(_np, 'generic', ())):
                    try:
                        return _convert(o.item(), seen)
                    except Exception:
                        return str(o)
                if isinstance(o, getattr(_np, 'ndarray', ())):
                    try:
                        return o.tolist()
                    except Exception:
                        return str(o)

            if _pd is not None:
                if isinstance(o, getattr(_pd, 'DataFrame', ())):
                    try:
                        return o.to_dict(orient='records')
                    except Exception:
                        return str(o)
                if isinstance(o, getattr(_pd, 'Series', ())):
                    try:
                        return o.to_list()
                    except Exception:
                        return str(o)

            if isinstance(o, (set, frozenset, tuple)):
                return [_convert(v, seen) for v in o]

            if isinstance(o, list):
                return [_convert(v, seen) for v in o]

            if isinstance(o, _Mapping):
                out: Dict[str, Any] = {}
                for k, v in o.items():
                    try:
                        sk = str(k)
                    except Exception:
                        sk = repr(k)
                    out[sk] = _convert(v, seen)
                return out

            if isinstance(o, Iterable) and not isinstance(o, (str, bytes, bytearray)):
                try:
                    return [_convert(v, seen) for v in o]
                except Exception:
                    return str(o)

            # Pydantic models (v2 then v1)
            try:
                if hasattr(o, 'model_dump') and _inspect.ismethod(getattr(o, 'model_dump')):
                    return _convert(o.model_dump(), seen)  # type: ignore
            except Exception:
                pass
            try:
                if hasattr(o, 'dict') and _inspect.ismethod(getattr(o, 'dict')):
                    return _convert(o.dict(), seen)  # type: ignore
            except Exception:
                pass

            # Objects with __json__ custom method
            try:
                if hasattr(o, '__json__'):
                    return _convert(o.__json__(), seen)  # type: ignore
            except Exception:
                pass

            # Objects with __dict__
            if hasattr(o, '__dict__'):
                try:
                    return _convert(vars(o), seen)
                except Exception:
                    return str(o)

            try:
                return str(o)
            except Exception:
                return f"<unserializable:{type(o).__name__}>"

        return _convert(obj, set())
