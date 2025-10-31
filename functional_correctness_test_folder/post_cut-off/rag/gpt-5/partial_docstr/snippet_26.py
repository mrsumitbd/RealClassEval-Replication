from typing import Any, Dict, Iterable
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from uuid import UUID
from enum import Enum
from pathlib import Path
from dataclasses import is_dataclass, asdict
from collections.abc import Mapping
import base64
import inspect


class DataConverter:
    '''Unified data conversion utilities.'''
    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        '''Flatten nested dictionary structure.
        Args:
            data: Nested dictionary
            prefix: Prefix for flattened keys
        Returns:
            Flattened dictionary
        '''
        if not isinstance(data, Mapping):
            raise TypeError('data must be a dictionary-like mapping')

        out: Dict[str, Any] = {}
        base = prefix.strip('.')

        def _flatten(obj: Any, parent_key: str) -> None:
            if isinstance(obj, Mapping):
                if not obj:
                    if parent_key:
                        out[parent_key] = {}
                    return
                for k, v in obj.items():
                    k_str = str(k)
                    new_key = f"{parent_key}.{k_str}" if parent_key else k_str
                    _flatten(v, new_key)
            elif isinstance(obj, (list, tuple)):
                if not obj:
                    if parent_key:
                        out[parent_key] = []
                    return
                for idx, item in enumerate(obj):
                    new_key = f"{parent_key}.{idx}" if parent_key else str(idx)
                    _flatten(item, new_key)
            else:
                if parent_key:
                    out[parent_key] = obj

        _flatten(data, base if base else '')
        return out

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        '''Extract model name from various data sources.
        Args:
            data: Data containing model information
            default: Default model name if not found
        Returns:
            Extracted model name
        '''
        if not isinstance(data, Mapping):
            return default

        # Direct checks at the root
        direct_keys = ('model', 'model_id', 'modelId', 'modelName',
                       'engine', 'deployment', 'deployment_id', 'name', 'id')
        for k in direct_keys:
            if k in data:
                v = data[k]
                if isinstance(v, str) and v.strip():
                    return v.strip()
                if isinstance(v, Mapping):
                    name = v.get('name') or v.get('id')
                    if isinstance(name, str) and name.strip():
                        return name.strip()

        # Known nested paths
        known_paths = [
            ('request', 'model'),
            ('options', 'model'),
            ('config', 'model'),
            ('params', 'model'),
            ('metadata', 'model'),
            ('settings', 'model'),
            ('body', 'model'),
            ('kwargs', 'model'),
            ('openai', 'model'),
            ('anthropic', 'model'),
            ('azure', 'deployment'),
            ('azure', 'deployment_id'),
            ('client', 'model'),
        ]
        for path in known_paths:
            ref = data
            ok = True
            for part in path:
                if isinstance(ref, Mapping) and part in ref:
                    ref = ref[part]
                else:
                    ok = False
                    break
            if ok:
                if isinstance(ref, str) and ref.strip():
                    return ref.strip()
                if isinstance(ref, Mapping):
                    name = ref.get('name') or ref.get('id') or ref.get('model')
                    if isinstance(name, str) and name.strip():
                        return name.strip()

        # Flatten and search by terminal token
        flat = DataConverter.flatten_nested_dict(data)
        terminal_candidates = ('model', 'model_id', 'modelname',
                               'deployment', 'deployment_id', 'engine', 'name', 'id')
        prioritized = ('model', 'model_id', 'modelname')

        # First pass: priority terminals
        for key, value in flat.items():
            last = key.lower().split('.')[-1].replace('-', '_')
            if last in prioritized:
                if isinstance(value, str) and value.strip():
                    return value.strip()
                if isinstance(value, Mapping):
                    name = value.get('name') or value.get('id')
                    if isinstance(name, str) and name.strip():
                        return name.strip()

        # Second pass: broader terminals
        for key, value in flat.items():
            last = key.lower().split('.')[-1].replace('-', '_')
            if last in terminal_candidates:
                if isinstance(value, str) and value.strip():
                    return value.strip()
                if isinstance(value, Mapping):
                    name = value.get('name') or value.get('id')
                    if isinstance(name, str) and name.strip():
                        return name.strip()

        # Heuristic: any key containing 'model' as a complete token (avoid matching 'message')
        for key, value in flat.items():
            tokens = []
            for part in key.split('.'):
                part = part.replace('-', '_')
                tokens.extend(part.split('_'))
            tokens_l = [t.lower() for t in tokens if t]
            if 'model' in tokens_l or 'modelid' in tokens_l:
                if isinstance(value, str) and value.strip():
                    return value.strip()

        # OpenAI-like response fallback
        if isinstance(data.get('model'), str) and data['model'].strip():
            return data['model'].strip()

        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        '''Convert object to JSON-serializable format.
        Args:
            obj: Object to convert
        Returns:
            JSON-serializable representation
        '''
        # Primitives
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj

        # datetime-like
        if isinstance(obj, (datetime, date, time)):
            try:
                return obj.isoformat()
            except Exception:
                return str(obj)
        if isinstance(obj, timedelta):
            return obj.total_seconds()

        # Decimal
        if isinstance(obj, Decimal):
            try:
                return float(obj)
            except Exception:
                return str(obj)

        # UUID
        if isinstance(obj, UUID):
            return str(obj)

        # Enum
        if isinstance(obj, Enum):
            value = obj.value
            return DataConverter.to_serializable(value)

        # Path
        if isinstance(obj, Path):
            return str(obj)

        # Bytes-like
        if isinstance(obj, (bytes, bytearray, memoryview)):
            b = bytes(obj)
            try:
                return b.decode('utf-8')
            except Exception:
                return 'base64:' + base64.b64encode(b).decode('ascii')

        # Dataclass
        if is_dataclass(obj):
            try:
                return DataConverter.to_serializable(asdict(obj))
            except Exception:
                return str(obj)

        # Pydantic (v2 -> model_dump, v1 -> dict)
        if hasattr(obj, 'model_dump') and callable(getattr(obj, 'model_dump')):
            try:
                return DataConverter.to_serializable(obj.model_dump())
            except Exception:
                pass
        if hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):
            try:
                return DataConverter.to_serializable(obj.dict())
            except Exception:
                pass

        # Numpy
        try:
            import numpy as np  # type: ignore
            if isinstance(obj, np.generic):
                return obj.item()
            if isinstance(obj, np.ndarray):
                return DataConverter.to_serializable(obj.tolist())
        except Exception:
            pass

        # Pandas
        try:
            import pandas as pd  # type: ignore
            if isinstance(obj, pd.DataFrame):
                return DataConverter.to_serializable(obj.to_dict(orient='records'))
            if isinstance(obj, pd.Series):
                return DataConverter.to_serializable(obj.to_list())
        except Exception:
            pass

        # Mapping
        if isinstance(obj, Mapping):
            out: Dict[str, Any] = {}
            for k, v in obj.items():
                key = k if isinstance(k, str) else str(k)
                out[key] = DataConverter.to_serializable(v)
            return out

        # Iterable (but not string/bytes already handled)
        if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes, bytearray)):
            try:
                return [DataConverter.to_serializable(item) for item in obj]
            except Exception:
                pass

        # Objects with serialization hooks
        for attr in ('__json__', 'to_json', 'to_dict'):
            if hasattr(obj, attr):
                fn = getattr(obj, attr)
                if callable(fn):
                    try:
                        val = fn()
                        return DataConverter.to_serializable(val)
                    except Exception:
                        continue

        # Callable: represent as string
        if callable(obj):
            try:
                name = getattr(obj, '__qualname__', None) or getattr(
                    obj, '__name__', None) or str(obj)
                module = getattr(obj, '__module__', None)
                return f"{module+'.' if module else ''}{name}"
            except Exception:
                return str(obj)

        # Fallback: repr
        try:
            return repr(obj)
        except Exception:
            return str(obj)
