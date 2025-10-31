from typing import Any, Dict, Iterable
from datetime import datetime, date, time
from decimal import Decimal
from uuid import UUID
from pathlib import Path
from dataclasses import is_dataclass, asdict
from enum import Enum
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
        flat: Dict[str, Any] = {}

        def _flatten(obj: Any, key_prefix: str) -> None:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_key = f"{key_prefix}.{k}" if key_prefix else str(k)
                    _flatten(v, new_key)
            elif isinstance(obj, (list, tuple)):
                for i, v in enumerate(obj):
                    new_key = f"{key_prefix}[{i}]" if key_prefix else f"[{i}]"
                    _flatten(v, new_key)
            else:
                flat[key_prefix] = obj

        _flatten(data, prefix if prefix else '')
        return flat

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        '''Extract model name from various data sources.
        Args:
            data: Data containing model information
            default: Default model name if not found
        Returns:
            Extracted model name
        '''
        # Direct checks for common top-level keys
        direct_keys = [
            'model',
            'model_name',
            'modelId',
            'model_id',
            'deployment',
            'deployment_id',
            'engine',
            'engine_id',
            'deploymentName',
            'deployment_name',
        ]
        for k in direct_keys:
            if k in data and isinstance(data[k], str) and data[k].strip():
                return data[k].strip()

        # Check common nested containers
        common_containers = ['request', 'config', 'options',
                             'params', 'metadata', 'headers', 'body', 'payload']
        for container in common_containers:
            if container in data and isinstance(data[container], dict):
                for k in direct_keys:
                    v = data[container].get(k)
                    if isinstance(v, str) and v.strip():
                        return v.strip()

        # Flatten and search with priority on exact-key suffixes
        flat = DataConverter.flatten_nested_dict(data)
        # Map of lower-case key to original value
        flat_items = [(k, v) for k, v in flat.items()
                      if isinstance(v, str) and v.strip()]

        # Priority exact suffixes
        exact_suffixes = [
            '.model',
            '.model_name',
            '.modelId',
            '.model_id',
            '.deployment',
            '.deployment_id',
            '.engine',
            '.engine_id',
            '.deploymentName',
            '.deployment_name',
        ]
        for suffix in exact_suffixes:
            for k, v in flat_items:
                if k.endswith(suffix):
                    return v.strip()

        # Any key that contains 'model'
        for k, v in flat_items:
            if 'model' in k.lower():
                return v.strip()

        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        '''Convert object to JSON-serializable format.
        Args:
            obj: Object to convert
        Returns:
            JSON-serializable representation
        '''
        seen: set[int] = set()

        def _conv(o: Any) -> Any:
            oid = id(o)
            if oid in seen:
                return f"<circular_ref {type(o).__name__}>"
            # Primitives
            if o is None or isinstance(o, (bool, int, float, str)):
                return o

            # Datetime and related types
            if isinstance(o, (datetime, date, time)):
                try:
                    return o.isoformat()
                except Exception:
                    return str(o)

            # Decimal, UUID, Path
            if isinstance(o, Decimal):
                # Convert safely: try int if integral, else float via string
                try:
                    if o == o.to_integral_value():
                        return int(o)
                    return float(o)
                except Exception:
                    return str(o)
            if isinstance(o, UUID):
                return str(o)
            if isinstance(o, Path):
                return str(o)

            # Bytes
            if isinstance(o, (bytes, bytearray, memoryview)):
                try:
                    return bytes(o).decode('utf-8')
                except Exception:
                    return "base64:" + base64.b64encode(bytes(o)).decode('ascii')

            # Enum
            if isinstance(o, Enum):
                return o.value if isinstance(o.value, (str, int, float, bool)) else str(o.value)

            # Dataclass
            if is_dataclass(o):
                seen.add(oid)
                try:
                    return {k: _conv(v) for k, v in asdict(o).items()}
                finally:
                    seen.discard(oid)

            # Numpy types (optional, avoid hard dependency)
            try:
                import numpy as np  # type: ignore
                if isinstance(o, (np.integer,)):
                    return int(o)
                if isinstance(o, (np.floating,)):
                    return float(o)
                if isinstance(o, (np.bool_,)):
                    return bool(o)
                if isinstance(o, (np.ndarray,)):
                    seen.add(oid)
                    try:
                        return [_conv(x) for x in o.tolist()]
                    finally:
                        seen.discard(oid)
            except Exception:
                pass

            # Pandas types (optional)
            try:
                import pandas as pd  # type: ignore
                if isinstance(o, (pd.Timestamp,)):
                    return o.isoformat()
                if isinstance(o, (pd.Timedelta,)):
                    return str(o)
                if isinstance(o, (pd.Series,)):
                    seen.add(oid)
                    try:
                        return _conv(o.to_dict())
                    finally:
                        seen.discard(oid)
                if isinstance(o, (pd.DataFrame,)):
                    seen.add(oid)
                    try:
                        return [_conv(rec) for rec in o.to_dict(orient='records')]
                    finally:
                        seen.discard(oid)
            except Exception:
                pass

            # Mapping
            if isinstance(o, dict):
                seen.add(oid)
                try:
                    return {str(k): _conv(v) for k, v in o.items()}
                finally:
                    seen.discard(oid)

            # Iterable (list, tuple, set, generators)
            if isinstance(o, (list, tuple, set)) or (not isinstance(o, (str, bytes, bytearray)) and isinstance(o, Iterable)):
                seen.add(oid)
                try:
                    return [_conv(i) for i in list(o)]
                finally:
                    seen.discard(oid)

            # to_dict / to_json methods
            for meth in ('to_dict', 'dict', 'to_json', 'json', 'model_dump'):
                if hasattr(o, meth) and callable(getattr(o, meth)):
                    try:
                        val = getattr(o, meth)()
                        # If to_json returns a JSON string, return it as string; otherwise continue conversion
                        if isinstance(val, str):
                            return val
                        return _conv(val)
                    except Exception:
                        continue

            # Exception
            if isinstance(o, BaseException):
                return {'error': type(o).__name__, 'message': str(o)}

            # Fallback: object __dict__
            if hasattr(o, '__dict__'):
                seen.add(oid)
                try:
                    return {str(k): _conv(v) for k, v in vars(o).items()}
                finally:
                    seen.discard(oid)

            # Last resort: repr
            try:
                return repr(o)
            except Exception:
                return f"<unserializable {type(o).__name__}>"

        return _conv(obj)
