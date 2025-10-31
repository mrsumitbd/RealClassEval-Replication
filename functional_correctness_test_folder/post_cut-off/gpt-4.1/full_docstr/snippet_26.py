
from typing import Any, Dict


class DataConverter:
    '''Unified data conversion utilities.'''

    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        '''Flatten nested dictionary structure.'''
        items = {}
        for k, v in data.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                items.update(DataConverter.flatten_nested_dict(v, new_key))
            else:
                items[new_key] = v
        return items

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        '''Extract model name from various data sources.'''
        # Common possible keys for model name
        possible_keys = ['model', 'model_name',
                         'modelName', 'model_id', 'modelId']
        for key in possible_keys:
            if key in data and isinstance(data[key], str):
                return data[key]
        # Sometimes model info is nested
        for key in data:
            if isinstance(data[key], dict):
                result = DataConverter.extract_model_name(data[key], default)
                if result != default:
                    return result
        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        '''Convert object to JSON-serializable format.'''
        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif isinstance(obj, dict):
            return {DataConverter.to_serializable(k): DataConverter.to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple, set)):
            return [DataConverter.to_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return DataConverter.to_serializable(vars(obj))
        elif hasattr(obj, '__slots__'):
            return {slot: DataConverter.to_serializable(getattr(obj, slot)) for slot in obj.__slots__}
        else:
            return str(obj)
