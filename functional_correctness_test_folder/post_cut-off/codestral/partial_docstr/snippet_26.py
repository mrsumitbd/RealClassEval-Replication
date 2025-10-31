
import json
from typing import Dict, Any


class DataConverter:
    '''Unified data conversion utilities.'''

    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
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
        model_keys = ['model', 'model_name', 'model_type']
        for key in model_keys:
            if key in data:
                return data[key]
        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif isinstance(obj, dict):
            return {k: DataConverter.to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [DataConverter.to_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return DataConverter.to_serializable(vars(obj))
        else:
            return str(obj)
