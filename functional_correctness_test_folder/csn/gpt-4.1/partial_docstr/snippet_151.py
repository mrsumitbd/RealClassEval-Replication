
import json


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
        self._serializable_properties = serializable_properties
        self._simple_properties = simple_properties

    def to_dict(self):
        result = {}
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
            if isinstance(value, list):
                result[prop] = [
                    v.to_dict() if hasattr(v, "to_dict") else v
                    for v in value
                ]
            elif hasattr(value, "to_dict"):
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
