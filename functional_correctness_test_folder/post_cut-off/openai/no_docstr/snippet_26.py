
from __future__ import annotations

import datetime
from typing import Any, Dict, Iterable, List, Tuple, Union


class DataConverter:
    @staticmethod
    def flatten_nested_dict(
        data: Dict[str, Any], prefix: str = ""
    ) -> Dict[str, Any]:
        """
        Recursively flatten a nested dictionary.

        Parameters
        ----------
        data : Dict[str, Any]
            The dictionary to flatten.
        prefix : str, optional
            Prefix to prepend to keys (used internally for recursion).

        Returns
        -------
        Dict[str, Any]
            A new dictionary with flattened keys.
        """
        flat: Dict[str, Any] = {}
        for key, value in data.items():
            full_key = f"{prefix}{key}" if prefix else key
            if isinstance(value, dict):
                flat.update(DataConverter.flatten_nested_dict(
                    value, f"{full_key}."))
            else:
                flat[full_key] = value
        return flat

    @staticmethod
    def extract_model_name(
        data: Dict[str, Any], default: str = "claude-3-5-sonnet"
    ) -> str:
        """
        Extract the model name from a dictionary.

        Parameters
        ----------
        data : Dict[str, Any]
            Dictionary that may contain a 'model' key.
        default : str, optional
            Default model name if none is found.

        Returns
        -------
        str
            The extracted model name or the default.
        """
        model = data.get("model")
        if isinstance(model, str):
            return model
        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        """
        Convert an arbitrary object into a JSON‑serialisable form.

        Parameters
        ----------
        obj : Any
            The object to convert.

        Returns
        -------
        Any
            A serialisable representation of the input.
        """
        # Handle basic types
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj

        # Handle datetime objects
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()

        # Handle collections
        if isinstance(obj, (list, tuple)):
            return [DataConverter.to_serializable(item) for item in obj]
        if isinstance(obj, set):
            return [DataConverter.to_serializable(item) for item in obj]

        # Handle dictionaries
        if isinstance(obj, dict):
            return {
                str(key): DataConverter.to_serializable(value)
                for key, value in obj.items()
            }

        # Handle objects with __dict__
        if hasattr(obj, "__dict__"):
            return DataConverter.to_serializable(vars(obj))

        # Fallback: convert to string
        return str(obj)
