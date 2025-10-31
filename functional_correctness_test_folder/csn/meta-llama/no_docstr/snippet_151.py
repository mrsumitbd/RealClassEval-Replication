
import json


class AdaptiveCardComponent:

    def __init__(self, serializable_properties, simple_properties):
        self.serializable_properties = serializable_properties
        self.simple_properties = simple_properties

    def to_dict(self):
        component_dict = {}
        for key, value in self.simple_properties.items():
            component_dict[key] = value

        for key, value in self.serializable_properties.items():
            if hasattr(value, 'to_dict'):
                component_dict[key] = value.to_dict()
            else:
                component_dict[key] = value

        return component_dict

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)
