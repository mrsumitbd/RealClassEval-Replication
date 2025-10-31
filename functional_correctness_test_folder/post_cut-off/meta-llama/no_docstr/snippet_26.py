
from typing import Dict, Any


class DataConverter:

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
        model_name = data.get('model_name') or data.get('model')
        return model_name if model_name else default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        if isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [DataConverter.to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: DataConverter.to_serializable(value) for key, value in obj.items()}
        else:
            try:
                return obj.__dict__
            except AttributeError:
                raise TypeError(
                    f"Object of type {obj.__class__.__name__} is not serializable")
