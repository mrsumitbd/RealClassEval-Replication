
import json
from collections.abc import Iterable


class AdaptiveCardComponent:
    '''
    Base class for all Adaptive Card elements.
    Each element should inherit from this class and specify which of its
    properties fall into the following two categories:
    * Simple properties are basic types (int, float, str, etc.).
    * Serializable properties are properties that can themselves be serialized.
      This includes lists of items (i.e. the 'body' field of the adaptive card)
      or single objects that also inherit from Serializable
    '''

    def __init__(self, serializable_properties, simple_properties):
        '''
        Initialize a serializable object.
        Args:
            serializable_properties(list): List of all serializable properties
            simple_properties(list): List of all simple properties.
        '''
        self._serializable_properties = serializable_properties
        self._simple_properties = simple_properties

    def to_dict(self):
        '''
        Serialize the element into a Python dictionary.
        The to_dict() method recursively serializes the object's data into
        a Python dictionary.
        Returns:
            dict: Dictionary representation of this element.
        '''
        result = {}

        # Simple properties
        for prop in self._simple_properties:
            if hasattr(self, prop):
                result[prop] = getattr(self, prop)

        # Serializable properties
        for prop in self._serializable_properties:
            if not hasattr(self, prop):
                continue
            value = getattr(self, prop)

            if value is None:
                result[prop] = None
                continue

            # Handle lists/iterables (but not strings)
            if isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
                serialized_list = []
                for item in value:
                    if hasattr(item, 'to_dict'):
                        serialized_list.append(item.to_dict())
                    else:
                        serialized_list.append(item)
                result[prop] = serialized_list
            # Handle dicts
            elif isinstance(value, dict):
                serialized_dict = {}
                for k, v in value.items():
                    if hasattr(v, 'to_dict'):
                        serialized_dict[k] = v.to_dict()
                    else:
                        serialized_dict[k] = v
                result[prop] = serialized_dict
            # Handle objects with to_dict
            elif hasattr(value, 'to_dict'):
                result[prop] = value.to_dict()
            else:
                result[prop] = value

        return result

    def to_json(self, **kwargs):
        '''
        Serialize the element into JSON text.
        Any keyword arguments provided are passed through the Python JSON
        encoder.
        '''
        return json.dumps(self.to_dict(), **kwargs)
