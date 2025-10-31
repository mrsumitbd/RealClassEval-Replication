import json
from collections.abc import Mapping, Sequence


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
        if serializable_properties is None:
            serializable_properties = []
        if simple_properties is None:
            simple_properties = []
        self._serializable_properties = tuple(serializable_properties)
        self._simple_properties = tuple(simple_properties)

    def _serialize_value(self, value):
        if value is None:
            return None

        if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
            return value.to_dict()

        if isinstance(value, Mapping):
            out = {}
            for k, v in value.items():
                sv = self._serialize_value(v)
                out[k] = sv
            return out

        # Treat sequences but not strings/bytes as collections
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            out_list = []
            for item in value:
                out_list.append(self._serialize_value(item))
            return out_list

        return value

    def to_dict(self):
        result = {}

        # Simple properties: add if not None
        for name in self._simple_properties:
            if not hasattr(self, name):
                continue
            val = getattr(self, name)
            if val is not None:
                result[name] = val

        # Serializable properties: serialize and add if not None
        for name in self._serializable_properties:
            if not hasattr(self, name):
                continue
            val = getattr(self, name)
            if val is None:
                continue
            serialized = self._serialize_value(val)
            if serialized is not None:
                result[name] = serialized

        return result

    def to_json(self, **kwargs):
        '''
        Serialize the element into JSON text.
        Any keyword arguments provided are passed through the Python JSON
        encoder.
        '''
        return json.dumps(self.to_dict(), **kwargs)
