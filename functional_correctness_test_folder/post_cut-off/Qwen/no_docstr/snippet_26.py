
from typing import Dict, Any, Union
import json


class DataConverter:

    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        flat_dict = {}
        for key, value in data.items():
            new_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flat_dict.update(
                    DataConverter.flatten_nested_dict(value, new_key))
            else:
                flat_dict[new_key] = value
        return flat_dict

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        return data.get('model_name', default)

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        if isinstance(obj, (dict, list, str, int, float, bool, type(None))):
            return obj
        elif hasattr(obj, '__dict__'):
            return DataConverter.to_serializable(obj.__dict__)
        else:
            raise TypeError(
                f"Object of type {obj.__class__.__name__} is not JSON serializable")
