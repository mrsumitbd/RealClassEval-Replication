
import base64
import datetime
from typing import Any, Dict, List, Tuple, Union


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
        for key, value in data.items():
            full_key = f'{prefix}.{key}' if prefix else key
            if isinstance(value, dict):
                flat.update(DataConverter.flatten_nested_dict(value, full_key))
            else:
                flat[full_key] = value
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
        # Flatten the dictionary to simplify key lookup
        flat = DataConverter.flatten_nested_dict(data)
        # Common keys that might hold the model name
        candidate_keys = [
            'model',
            'model_name',
            'name',
            'model_info.model',
            'model_info.model_name',
            'model_info.name',
            'model_details.model',
            'model_details.model_name',
            'model_details.name',
        ]
        for key in candidate_keys:
            if key in flat and isinstance(flat[key], str):
                return flat[key]
        # Fallback: search any string value that looks like a model name
        for value in flat.values():
            if isinstance(value, str) and value:
                return value
        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        '''Convert object to JSON-serializable format.
        Args:
            obj: Object to convert
        Returns:
            JSON-serializable representation
        '''
        if obj is None:
            return None
        if isinstance(obj, (str, int, float, bool)):
            return obj
        if isinstance(obj, (list, tuple)):
            return [DataConverter.to_serializable(v) for v in obj]
        if isinstance(obj, dict):
            return {k: DataConverter.to_serializable(v) for k, v in obj.items()}
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, set):
            return [DataConverter.to_serializable(v) for v in obj]
        if isinstance(obj, bytes):
            # Encode bytes as base64 string
            return base64.b64encode(obj).decode('utf-8')
        # Try to serialize objects with __dict__
        if hasattr(obj, '__dict__'):
            return DataConverter.to_serializable(obj.__dict__)
        # Fallback to string representation
        return str(obj)
