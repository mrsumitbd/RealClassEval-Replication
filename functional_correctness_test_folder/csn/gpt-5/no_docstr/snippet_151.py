import json


class AdaptiveCardComponent:

    def __init__(self, serializable_properties, simple_properties):
        self._serializable_properties = tuple(serializable_properties or ())
        self._simple_properties = tuple(simple_properties or ())

    def _serialize_value(self, value):
        if value is None:
            return None
        if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
            return value.to_dict()
        if isinstance(value, (list, tuple, set)):
            return [self._serialize_value(v) for v in value if v is not None]
        if isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items() if v is not None}
        return value

    def to_dict(self):
        result = {}
        for prop in self._simple_properties:
            if hasattr(self, prop):
                val = getattr(self, prop)
                if val is not None:
                    result[prop] = val
        for prop in self._serializable_properties:
            if hasattr(self, prop):
                val = getattr(self, prop)
                if val is not None:
                    result[prop] = self._serialize_value(val)
        return result

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)
