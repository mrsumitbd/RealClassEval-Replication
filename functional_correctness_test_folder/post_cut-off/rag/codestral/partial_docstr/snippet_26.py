
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
        flattened = {}
        for key, value in data.items():
            new_key = f"{prefix}{key}" if prefix else key
            if isinstance(value, dict):
                flattened.update(
                    DataConverter.flatten_nested_dict(value, f"{new_key}."))
            else:
                flattened[new_key] = value
        return flattened

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        '''Extract model name from various data sources.
        Args:
            data: Data containing model information
            default: Default model name if not found
        Returns:
            Extracted model name
        '''
        if 'model' in data:
            return data['model']
        if 'model_name' in data:
            return data['model_name']
        if 'model_id' in data:
            return data['model_id']
        if 'model_version' in data:
            return data['model_version']
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
            return [DataConverter.to_serializable(item) for item in obj]
        if hasattr(obj, '__dict__'):
            return DataConverter.to_serializable(obj.__dict__)
        if hasattr(obj, 'to_dict'):
            return DataConverter.to_serializable(obj.to_dict())
        if hasattr(obj, '__str__'):
            return str(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
