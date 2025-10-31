
import json
from typing import Dict, Any


class DataConverter:

    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
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
        model_name = data.get('model', default)
        if isinstance(model_name, dict):
            model_name = model_name.get('name', default)
        return model_name

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [DataConverter.to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: DataConverter.to_serializable(value) for key, value in obj.items()}
        else:
            try:
                return json.loads(json.dumps(obj))
            except (TypeError, OverflowError):
                return str(obj)
