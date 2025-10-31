
import json


class AdaptiveCardComponent:

    def __init__(self, serializable_properties, simple_properties):
        self.serializable_properties = serializable_properties
        self.simple_properties = simple_properties

    def to_dict(self):
        result = {}
        for prop in self.serializable_properties:
            if hasattr(self, prop):
                value = getattr(self, prop)
                if hasattr(value, 'to_dict'):
                    result[prop] = value.to_dict()
                else:
                    result[prop] = value
        for prop in self.simple_properties:
            if hasattr(self, prop):
                result[prop] = getattr(self, prop)
        return result

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)
