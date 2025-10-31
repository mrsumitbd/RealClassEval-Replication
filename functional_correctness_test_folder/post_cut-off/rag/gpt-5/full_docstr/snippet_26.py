from typing import Any, Dict, Mapping, Iterable
from collections.abc import Mapping as ABCMapping, Iterable as ABCIterable
import dataclasses
import datetime
import decimal
import enum
import uuid
import base64
from pathlib import Path


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
        result: Dict[str, Any] = {}

        def _join(parent: str, key: str) -> str:
            if parent:
                if parent.endswith('.'):
                    return f'{parent}{key}'
                return f'{parent}.{key}'
            return key

        def _flatten(obj: Any, parent_key: str) -> None:
            if isinstance(obj, dict):
                if not obj and parent_key:
                    result[parent_key] = {}
                    return
                for k, v in obj.items():
                    nk = _join(parent_key, str(k))
                    _flatten(v, nk)
            elif isinstance(obj, (list, tuple)):
                if not obj and parent_key:
                    result[parent_key] = []
                    return
                for i, v in enumerate(obj):
                    nk = _join(parent_key, str(i))
                    _flatten(v, nk)
            else:
                if parent_key:
                    result[parent_key] = obj

        _flatten(data, prefix.strip('.') if prefix else '')
        return result

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        '''Extract model name from various data sources.
        Args:
            data: Data containing model information
            default: Default model name if not found
        Returns:
            Extracted model name
        '''
        if not isinstance(data, dict) or not data:
            return default

        # Quick top-level checks
        direct_keys = [
            'model', 'model_name', 'modelName', 'model_id', 'modelId',
            'deployment', 'deployment_name', 'deploymentName',
            'deployment_id', 'deploymentId', 'engine', 'name'
        ]
        for k in direct_keys:
            if k in data and isinstance(data[k], str) and data[k].strip():
                if k == 'name':
                    # Only accept top-level 'name' if there is no better candidate below
                    # We'll fall back to it later if needed
                    continue
                return data[k].strip()

        flattened = DataConverter.flatten_nested_dict(data)
        # Normalize keys
        norm_map: Dict[str, str] = {}
        for k, v in flattened.items():
            if isinstance(v, str) and v.strip():
                nk = str(k).replace('-', '_').lower()
                norm_map[nk] = v.strip()

        # Priority candidates (match exact or suffix)
        candidates = [
            'model',
            'request.model',
            'parameters.model',
            'params.model',
            'config.model',
            'settings.model',
            'options.model',
            'generation_config.model',
            'api.model',
            'client.model',
            'data.model',
            'model.name',
            'model_id',
            'modelid',
            'model_name',
            'modelname',
            'model.id',
            'deployment',
            'deployment_name',
            'deployment_id',
            'engine',
        ]

        keys_in_order = list(norm_map.keys())

        # Search in priority order
        for cand in candidates:
            dot_cand = f'.{cand}'
            for k in keys_in_order:
                if k == cand or k.endswith(dot_cand):
                    return norm_map[k]

        # Consider generic "name" only when associated with "model" path
        for k in keys_in_order:
            if (k == 'name' or k.endswith('.name')) and 'model' in k:
                return norm_map[k]

        # Fallback: any key containing 'model'
        for k in keys_in_order:
            if 'model' in k:
                return norm_map[k]

        # Last resort: top-level 'name'
        if isinstance(data.get('name'), str) and data['name'].strip():
            return data['name'].strip()

        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        '''Convert object to JSON-serializable format.
        Args:
            obj: Object to convert
        Returns:
            JSON-serializable representation
        '''
        primitive_types = (str, int, float, bool, type(None))

        def _is_primitive(x: Any) -> bool:
            return isinstance(x, primitive_types)

        seen: set[int] = set()

        def _convert(o: Any) -> Any:
            if _is_primitive(o):
                return o

            oid = id(o)
            # Only track potentially recursive structures
            track_recursion = isinstance(
                o, (dict, list, tuple, set)) or hasattr(o, '__dict__')
            if track_recursion:
                if oid in seen:
                    return str(o)
                seen.add(oid)

            # Dataclasses
            if dataclasses.is_dataclass(o):
                return _convert(dataclasses.asdict(o))

            # Enums
            if isinstance(o, enum.Enum):
                return _convert(o.value)

            # Date/time
            if isinstance(o, (datetime.datetime, datetime.date, datetime.time)):
                try:
                    return o.isoformat()
                except Exception:
                    return str(o)

            # UUID
            if isinstance(o, uuid.UUID):
                return str(o)

            # Decimal
            if isinstance(o, decimal.Decimal):
                # Use string to avoid JSON NaN/Inf issues and preserve precision
                return str(o)

            # Bytes-like
            if isinstance(o, (bytes, bytearray, memoryview)):
                try:
                    return base64.b64encode(bytes(o)).decode('ascii')
                except Exception:
                    return str(o)

            # Path-like
            if isinstance(o, Path):
                return str(o)

            # Mappings
            if isinstance(o, (Mapping, ABCMapping)):
                out: Dict[str, Any] = {}
                for k, v in o.items():
                    try:
                        sk = str(k)
                    except Exception:
                        sk = repr(k)
                    out[sk] = _convert(v)
                return out

            # Iterables (exclude strings/bytes already handled)
            if isinstance(o, (ABCIterable, list, tuple, set)) and not isinstance(o, (str, bytes, bytearray)):
                return [_convert(i) for i in o]

            # Objects with serialization hooks
            for attr in ('to_dict', 'model_dump', 'dict'):
                meth = getattr(o, attr, None)
                if callable(meth):
                    try:
                        return _convert(meth())
                    except Exception:
                        pass

            # Generic object: try __dict__
            dct = getattr(o, '__dict__', None)
            if isinstance(dct, dict):
                out: Dict[str, Any] = {}
                for k, v in dct.items():
                    if callable(v):
                        continue
                    out[str(k)] = _convert(v)
                return out

            # Fallback to string
            return str(o)

        return _convert(obj)
