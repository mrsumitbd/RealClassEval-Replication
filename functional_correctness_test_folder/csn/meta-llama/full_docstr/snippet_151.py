
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
        '''
        Initialize a serializable object.
        Args:
            serializable_properties(list): List of all serializable properties
            simple_properties(list): List of all simple properties.
        '''
        self.serializable_properties = serializable_properties
        self.simple_properties = simple_properties

    def to_dict(self):
        '''
        Serialize the element into a Python dictionary.
        The to_dict() method recursively serializes the object's data into
        a Python dictionary.
        Returns:
            dict: Dictionary representation of this element.
        '''
        data = {}
        for prop in self.simple_properties:
            if hasattr(self, prop):
                data[prop] = getattr(self, prop)
        for prop in self.serializable_properties:
            if hasattr(self, prop):
                value = getattr(self, prop)
                if isinstance(value, list):
                    data[prop] = [item.to_dict() if hasattr(
                        item, 'to_dict') else item for item in value]
                else:
                    data[prop] = value.to_dict() if hasattr(
                        value, 'to_dict') else value
        return {k: v for k, v in data.items() if v is not None}

    def to_json(self, **kwargs):
        '''
        Serialize the element into JSON text.
        Any keyword arguments provided are passed through the Python JSON
        encoder.
        '''
        return json.dumps(self.to_dict(), **kwargs)
