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
        self._serializable_properties = list(serializable_properties or [])
        self._simple_properties = list(simple_properties or [])

    def _serialize_value(self, value):
        if value is None:
            return None
        if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
            return value.to_dict()
        if isinstance(value, (list, tuple)):
            serialized_list = []
            for item in value:
                if item is None:
                    serialized_list.append(None)
                elif hasattr(item, "to_dict") and callable(getattr(item, "to_dict")):
                    serialized_list.append(item.to_dict())
                else:
                    serialized_list.append(item)
            return serialized_list
        return value

    def to_dict(self):
        '''
        Serialize the element into a Python dictionary.
        The to_dict() method recursively serializes the object's data into
        a Python dictionary.
        Returns:
            dict: Dictionary representation of this element.
        '''
        result = {}

        for prop in self._simple_properties:
            if hasattr(self, prop):
                value = getattr(self, prop)
                if value is not None:
                    result[prop] = value

        for prop in self._serializable_properties:
            if hasattr(self, prop):
                value = getattr(self, prop)
                if value is None:
                    continue
                serialized = self._serialize_value(value)
                result[prop] = serialized

        return result

    def to_json(self, **kwargs):
        '''
        Serialize the element into JSON text.
        Any keyword arguments provided are passed through the Python JSON
        encoder.
        '''
        return json.dumps(self.to_dict(), **kwargs)
