from typing import Any, Dict, List, Optional, Union
from datetime import datetime

class DataConverter:
    """Unified data conversion utilities."""

    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str='') -> Dict[str, Any]:
        """Flatten nested dictionary structure.

        Args:
            data: Nested dictionary
            prefix: Prefix for flattened keys

        Returns:
            Flattened dictionary
        """
        result: Dict[str, Any] = {}
        for key, value in data.items():
            new_key = f'{prefix}.{key}' if prefix else key
            if isinstance(value, dict):
                result.update(DataConverter.flatten_nested_dict(value, new_key))
            else:
                result[new_key] = value
        return result

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str='claude-3-5-sonnet') -> str:
        """Extract model name from various data sources.

        Args:
            data: Data containing model information
            default: Default model name if not found

        Returns:
            Extracted model name
        """
        model_candidates: List[Optional[Any]] = [data.get('message', {}).get('model'), data.get('model'), data.get('Model'), data.get('usage', {}).get('model'), data.get('request', {}).get('model')]
        for candidate in model_candidates:
            if candidate and isinstance(candidate, str):
                return candidate
        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        """Convert object to JSON-serializable format.

        Args:
            obj: Object to convert

        Returns:
            JSON-serializable representation
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, dict):
            return {k: DataConverter.to_serializable(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [DataConverter.to_serializable(item) for item in obj]
        return obj