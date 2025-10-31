
from typing import Dict, Any
import json


class DataConverter:
    '''Unified data conversion utilities.'''
    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        flattened = {}
        for key, value in data.items():
            new_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flattened.update(
                    DataConverter.flatten_nested_dict(value, new_key))
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
        model_keys = ['model', 'model_name',
                      'modelName', 'model_id', 'modelId']
        for key in model_keys:
            if key in data:
                return data[key]
        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        '''Convert object to JSON-serializable format.
        Args:
            obj: Object to convert
        Returns:
            JSON-serializable representation
        '''
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, dict):
            return {key: DataConverter.to_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [DataConverter.to_serializable(item) for item in obj]
        else:
            return str(obj)
