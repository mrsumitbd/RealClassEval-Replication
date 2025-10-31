
import json
from typing import Any, Dict, Optional


class AdaptiveCardComponent:
    """
    A lightweight base class for Adaptive Card components.

    Parameters
    ----------
    serializable_properties : Optional[Dict[str, Any]]
        Properties that are themselves objects with a ``to_dict`` method.
    simple_properties : Optional[Dict[str, Any]]
        Simple key/value pairs that can be serialised directly.
    """

    def __init__(
        self,
        serializable_properties: Optional[Dict[str, Any]] = None,
        simple_properties: Optional[Dict[str, Any]] = None,
    ):
        self.serializable_properties = serializable_properties or {}
        self.simple_properties = simple_properties or {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the component into a plain dictionary.

        Returns
        -------
        dict
            A dictionary representation of the component.
        """
        result: Dict[str, Any] = {}

        # Handle serializable properties
        for key, value in self.serializable_properties.items():
            if hasattr(value, "to_dict") and callable(value.to_dict):
                result[key] = value.to_dict()
            else:
                # Fallback: use the value directly
                result[key] = value

        # Handle simple properties
        for key, value in self.simple_properties.items():
            result[key] = value

        return result

    def to_json(self, **kwargs) -> str:
        """
        Convert the component into a JSON string.

        Parameters
        ----------
        **kwargs
            Keyword arguments passed to :func:`json.dumps`.

        Returns
        -------
        str
            JSON representation of the component.
        """
        return json.dumps(self.to_dict(), **kwargs)
