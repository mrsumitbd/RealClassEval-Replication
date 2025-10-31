
import json


class AdaptiveCardComponent:

    def __init__(self, serializable_properties, simple_properties):
        self.serializable_properties = serializable_properties
        self.simple_properties = simple_properties

    def to_dict(self):
        result = {}
        for prop in self.serializable_properties:
            value = getattr(self, prop)
            if isinstance(value, AdaptiveCardComponent):
                result[prop] = value.to_dict()
            elif isinstance(value, list):
                result[prop] = [item.to_dict() if isinstance(
                    item, AdaptiveCardComponent) else item for item in value]
            else:
                result[prop] = value
        for prop in self.simple_properties:
            result[prop] = getattr(self, prop)
        return result

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)
