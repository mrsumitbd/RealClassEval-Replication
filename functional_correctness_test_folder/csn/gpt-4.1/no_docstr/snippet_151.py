
import json


class AdaptiveCardComponent:

    def __init__(self, serializable_properties, simple_properties):
        self.serializable_properties = serializable_properties
        self.simple_properties = simple_properties

    def to_dict(self):
        result = {}
        for key, value in self.simple_properties.items():
            result[key] = value
        for key, value in self.serializable_properties.items():
            if hasattr(value, "to_dict"):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if hasattr(item, "to_dict") else item
                    for item in value
                ]
            else:
                result[key] = value
        return result

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)
