
import json
from typing import Any, Dict


class DataConverter:
    """Unified data conversion utilities."""

    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        """Flatten nested dictionary structure.

        Args:
            data: Nested dictionary
            prefix: Prefix for flattened keys

        Returns:
            Flattened dictionary
        """
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
        """Extract model name from various data sources.

        Args:
            data: Data containing model information
            default: Default model name if not found

        Returns:
            Extracted model name
        """
        model_name = data.get('model_name') or data.get(
            'model') or data.get('model_id')
        return model_name if model_name else default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        """Convert object to JSON-serializable format.

        Args:
            obj: Object to convert

        Returns:
            JSON-serializable representation
        """
        if isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [DataConverter.to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: DataConverter.to_serializable(value) for key, value in obj.items()}
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        else:
            try:
                return json.loads(json.dumps(obj))
            except TypeError:
                return str(obj)
