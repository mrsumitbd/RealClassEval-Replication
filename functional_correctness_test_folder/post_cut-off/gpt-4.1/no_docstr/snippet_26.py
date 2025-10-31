
from typing import Any, Dict


class DataConverter:

    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        result = {}
        for k, v in data.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                result.update(DataConverter.flatten_nested_dict(v, key))
            else:
                result[key] = v
        return result

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        if 'model' in data and isinstance(data['model'], str):
            return data['model']
        for k, v in data.items():
            if isinstance(v, dict):
                name = DataConverter.extract_model_name(v, default)
                if name != default:
                    return name
        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif isinstance(obj, dict):
            return {DataConverter.to_serializable(k): DataConverter.to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple, set)):
            return [DataConverter.to_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return DataConverter.to_serializable(vars(obj))
        else:
            return str(obj)
