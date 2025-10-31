
from __future__ import annotations

from datetime import date, datetime, time
from typing import Any, Dict, Iterable, List, Tuple, Union


class DataConverter:
    '''Unified data conversion utilities.'''

    @staticmethod
    def flatten_nested_dict(
        data: Dict[str, Any], prefix: str = ''
    ) -> Dict[str, Any]:
        """
        Recursively flatten a nested dictionary.

        Parameters
        ----------
        data : Dict[str, Any]
            The dictionary to flatten.
        prefix : str, optional
            Prefix to prepend to keys (default: '').

        Returns
        -------
        Dict[str, Any]
            A flattened dictionary with dot‑separated keys.
        """
        flat: Dict[str, Any] = {}
        for key, value in data.items():
            full_key = f'{prefix}.{key}' if prefix else key
            if isinstance(value, dict):
                flat.update(DataConverter.flatten_nested_dict(value, full_key))
            else:
                flat[full_key] = value
        return flat

    @staticmethod
    def extract_model_name(
        data: Dict[str, Any], default: str = 'claude-3-5-sonnet'
    ) -> str:
        """
        Extract a model name from a dictionary that may contain the name
        under various keys or nested structures.

        Parameters
        ----------
        data : Dict[str, Any]
            Dictionary that may contain model information.
        default : str, optional
            Default model name if none is found (default: 'claude-3-5-sonnet').

        Returns
        -------
        str
            The extracted model name or the default.
        """
        # Known keys that might hold the model name
        candidate_keys = {
            'model',
            'model_name',
            'name',
            'model_id',
            'modelId',
            'modelName',
            'model_name',
            'model-id',
            'modelId',
        }

        def _search(d: Any) -> Union[str, None]:
            if isinstance(d, dict):
                for k, v in d.items():
                    if k in candidate_keys and isinstance(v, str):
                        return v
                    # Recurse into nested dicts
                    if isinstance(v, dict):
                        res = _search(v)
                        if res:
                            return res
                    # Recurse into lists/tuples
                    if isinstance(v, (list, tuple)):
                        for item in v:
                            res = _search(item)
                            if res:
                                return res
            elif isinstance(d, (list, tuple)):
                for item in d:
                    res = _search(item)
                    if res:
                        return res
            return None

        result = _search(data)
        return result if result else default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        """
        Convert an arbitrary Python object into a JSON‑serializable form.

        Parameters
        ----------
        obj : Any
            The object to convert.

        Returns
        -------
        Any
            A JSON‑serializable representation of the input.
        """
        # Primitive types are already serializable
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj

        # Handle collections
        if isinstance(obj, (list, tuple)):
            return [DataConverter.to_serializable(item) for item in obj]
        if isinstance(obj, set):
            return [DataConverter.to_serializable(item) for item in obj]

        # Handle dictionaries
        if isinstance(obj, dict):
            return {
                str(k): DataConverter.to_serializable(v) for k, v in obj.items()
            }

        # Handle datetime objects
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()

        # Handle bytes
        if isinstance(obj, bytes):
            try:
                return obj.decode('utf-8')
            except Exception:
                return obj.decode('latin1')

        # Handle objects with __dict__
        if hasattr(obj, '__dict__'):
            return DataConverter.to_serializable(vars(obj))

        # Fallback: convert to string
        return str(obj)
