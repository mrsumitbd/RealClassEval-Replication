
from typing import Dict, Any, Union
import json


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
        flattened_data = {}
        for key, value in data.items():
            new_key = f"{prefix}{key}" if prefix else key
            if isinstance(value, dict):
                flattened_data.update(
                    DataConverter.flatten_nested_dict(value, f"{new_key}."))
            else:
                flattened_data[new_key] = value
        return flattened_data

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        '''Extract model name from various data sources.
        Args:
            data: Data containing model information
            default: Default model name if not found
        Returns:
            Extracted model name
        '''
        model_name = default
        if 'model' in data:
            model_name = data['model']
        elif 'model_name' in data:
            model_name = data['model_name']
        elif 'model_info' in data and 'name' in data['model_info']:
            model_name = data['model_info']['name']
        return model_name

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
        elif isinstance(obj, dict):
            return {key: DataConverter.to_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple, set)):
            return [DataConverter.to_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return DataConverter.to_serializable(obj.__dict__)
        else:
            return str(obj)
