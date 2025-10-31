
import json
from typing import Any, Dict, List, Union


class AdaptiveCardComponent:
    """
    Base class for all Adaptive Card elements.
    Each element should inherit from this class and specify which of its
    properties fall into the following two categories:
    * Simple properties are basic types (int, float, str, etc.).
    * Serializable properties are properties that can themselves be serialized.
      This includes lists of items (i.e. the 'body' field of the adaptive card)
      or single objects that also inherit from Serializable
    """

    def __init__(self, serializable_properties: List[str], simple_properties: List[str]):
        """
        Parameters
        ----------
        serializable_properties : List[str]
            Names of attributes that are themselves serializable objects or lists of such objects.
        simple_properties : List[str]
            Names of attributes that are simple (primitive) types.
        """
        self._serializable_properties = serializable_properties
        self._simple_properties = simple_properties

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the component into a dictionary representation suitable for JSON serialization.
        """
        result: Dict[str, Any] = {}

        # Handle simple properties
        for prop in self._simple_properties:
            value = getattr(self, prop, None)
            if value is not None:
                result[prop] = value

        # Handle serializable properties
        for prop in self._serializable_properties:
            value = getattr(self, prop, None)
            if value is None:
                continue

            # If it's a list, serialize each element
            if isinstance(value, list):
                serialized_list = []
                for item in value:
                    if hasattr(item, "to_dict") and callable(item.to_dict):
                        serialized_list.append(item.to_dict())
                    else:
                        serialized_list.append(item)
                result[prop] = serialized_list
            # If it's a single serializable object
            elif hasattr(value, "to_dict") and callable(value.to_dict):
                result[prop] = value.to_dict()
            else:
                # Fallback: use the value as-is
                result[prop] = value

        return result

    def to_json(self, **kwargs: Any) -> str:
        """
        Serialize the element into JSON text.
        Any keyword arguments provided are passed through the Python JSON encoder.
        """
        return json.dumps(self.to_dict(), **kwargs)
