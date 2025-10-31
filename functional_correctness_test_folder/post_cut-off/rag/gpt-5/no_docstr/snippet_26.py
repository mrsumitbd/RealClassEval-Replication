from typing import Any, Dict, Iterable, Mapping
import datetime
import decimal
import base64
import uuid
import pathlib
from enum import Enum
from dataclasses import is_dataclass, asdict
from collections.abc import Generator


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

        def _flatten(obj: Any, parent_key: str = '') -> None:
            if isinstance(obj, Mapping):
                for k, v in obj.items():
                    new_key = f"{parent_key}.{k}" if parent_key else str(k)
                    _flatten(v, new_key)
            elif isinstance(obj, (list, tuple)):
                for i, v in enumerate(obj):
                    new_key = f"{parent_key}.{i}" if parent_key else str(i)
                    _flatten(v, new_key)
            else:
                # Apply prefix to the final key if provided
                key = parent_key
                if prefix:
                    if prefix.endswith(('.', '-', '_', '/')):
                        key = f"{prefix}{key}"
                    else:
                        key = f"{prefix}.{key}" if key else prefix.rstrip('.')
                result[key] = obj

        # If data is not a Mapping, still handle gracefully by returning a single-item dict
        if not isinstance(data, Mapping):
            key = prefix.rstrip('.') or ''
            if key == '':
                key = 'value'
            result[key] = data
            return result

        _flatten(data, '')
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
        if not isinstance(data, Mapping):
            return default

        flattened = DataConverter.flatten_nested_dict(data)

        def pick_value(val: Any) -> str | None:
            if isinstance(val, str) and val.strip():
                return val.strip()
            if isinstance(val, Mapping):
                # Common nested forms
                for k in ('model', 'name', 'model_name', 'id', 'identifier'):
                    v = val.get(k)
                    if isinstance(v, str) and v.strip():
                        return v.strip()
            return None

        # Priority exact keys (most common first)
        exact_candidates = [
            'model', 'model_name', 'modelName', 'model_id', 'modelId',
        ]
        for k, v in flattened.items():
            last = k.split('.')[-1]
            if last in exact_candidates:
                picked = pick_value(v)
                if picked:
                    return picked

        # Secondary synonyms often used by providers
        synonym_candidates = [
            'deployment', 'deployment_name', 'deploymentName',
            'engine', 'engine_name', 'engineName', 'target_model', 'targetModel',
        ]
        for k, v in flattened.items():
            last = k.split('.')[-1]
            if last in synonym_candidates:
                picked = pick_value(v)
                if picked:
                    return picked

        # Heuristic fallback: any key containing "model"
        for k, v in flattened.items():
            if 'model' in k.lower():
                picked = pick_value(v)
                if picked:
                    return picked

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

        # Dataclasses
        if is_dataclass(obj):
            return DataConverter.to_serializable(asdict(obj))

        # Enums
        if isinstance(obj, Enum):
            try:
                return DataConverter.to_serializable(obj.value)
            except Exception:
                return obj.name

        # UUID
        if isinstance(obj, uuid.UUID):
            return str(obj)

        # Path-like
        if isinstance(obj, (pathlib.Path,)):
            return str(obj)

        # Decimal
        if isinstance(obj, decimal.Decimal):
            # Convert to string to avoid precision loss
            return format(obj, 'f')

        # Datetime/date/time
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            try:
                return obj.isoformat()
            except Exception:
                return str(obj)

        # Bytes / bytearray
        if isinstance(obj, (bytes, bytearray)):
            try:
                return base64.b64encode(bytes(obj)).decode('ascii')
            except Exception:
                return str(obj)

        # numpy scalars / arrays without importing numpy
        mod = getattr(obj.__class__, '__module__', '')
        if 'numpy' in mod:
            # numpy scalar
            if hasattr(obj, 'item'):
                try:
                    return DataConverter.to_serializable(obj.item())
                except Exception:
                    pass
            # numpy array
            if hasattr(obj, 'tolist'):
                try:
                    return DataConverter.to_serializable(obj.tolist())
                except Exception:
                    pass

        # Pydantic v2 model
        if hasattr(obj, 'model_dump') and callable(getattr(obj, 'model_dump')):
            try:
                return DataConverter.to_serializable(obj.model_dump(by_alias=True))
            except Exception:
                pass

        # Pydantic v1 model
        if hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):
            try:
                return DataConverter.to_serializable(obj.dict(by_alias=True))
            except Exception:
                pass

        # Custom to_dict
        if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            try:
                return DataConverter.to_serializable(obj.to_dict())
            except Exception:
                pass

        # Mapping
        if isinstance(obj, Mapping):
            new_dict: Dict[str, Any] = {}
            for k, v in obj.items():
                # Ensure keys are strings
                key_str = str(k)
                new_dict[key_str] = DataConverter.to_serializable(v)
            return new_dict

        # Iterable (including generators), but not strings/bytes handled above
        if isinstance(obj, (Iterable, Generator)) and not isinstance(obj, (str, bytes, bytearray)):
            try:
                return [DataConverter.to_serializable(x) for x in obj]
            except Exception:
                pass

        # Fallback to object __dict__ if available
        if hasattr(obj, '__dict__'):
            try:
                return DataConverter.to_serializable(vars(obj))
            except Exception:
                pass

        # Final fallback: string representation
        return str(obj)
