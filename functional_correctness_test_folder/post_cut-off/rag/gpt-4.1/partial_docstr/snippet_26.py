import json
from typing import Any, Dict


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
        items = {}
        for k, v in data.items():
            new_key = f"{prefix}{k}" if prefix == '' else f"{prefix}.{k}"
            if isinstance(v, dict):
                items.update(DataConverter.flatten_nested_dict(v, new_key))
            else:
                items[new_key] = v
        return items

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        '''Extract model name from various data sources.
        Args:
            data: Data containing model information
            default: Default model name if not found
        Returns:
            Extracted model name
        '''
        # Common keys to check for model name
        keys = ['model', 'model_name', 'modelName', 'name']
        for key in keys:
            if key in data and isinstance(data[key], str):
                return data[key]
        # Sometimes model info is nested
        for key in data:
            if isinstance(data[key], dict):
                result = DataConverter.extract_model_name(
                    data[key], default=None)
                if result:
                    return result
        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        '''Convert object to JSON-serializable format.
        Args:
            obj: Object to convert
        Returns:
            JSON-serializable representation
        '''
        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        if isinstance(obj, dict):
            return {k: DataConverter.to_serializable(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple, set)):
            return [DataConverter.to_serializable(v) for v in obj]
        if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            return DataConverter.to_serializable(obj.to_dict())
        if hasattr(obj, '__dict__'):
            return DataConverter.to_serializable(vars(obj))
        try:
            return str(obj)
        except Exception:
            return None
