
from typing import Dict, Any
import json


class DataConverter:
    '''Unified data conversion utilities.'''
    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        result = {}
        for key, value in data.items():
            new_key = f"{prefix}{key}" if prefix else key
            if isinstance(value, dict):
                result.update(DataConverter.flatten_nested_dict(
                    value, new_key + '.'))
            else:
                result[new_key] = value
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
        model_name = data.get('model_name') or data.get(
            'model') or data.get('model_id')
        return model_name or default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        '''Convert object to JSON-serializable format.
        Args:
            obj: Object to convert
        Returns:
            JSON-serializable representation
        '''
        try:
            json.dumps(obj)
            return obj
        except TypeError:
            if hasattr(obj, '__dict__'):
                return DataConverter.to_serializable(obj.__dict__)
            elif hasattr(obj, '__iter__'):
                return [DataConverter.to_serializable(item) for item in obj]
            else:
                return str(obj)
