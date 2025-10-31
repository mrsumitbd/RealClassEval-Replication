import json
import enum

class AdaptiveCardComponent:
    """
    Base class for all Adaptive Card elements.

    Each element should inherit from this class and specify which of its
    properties fall into the following two categories:

    * Simple properties are basic types (int, float, str, etc.).

    * Serializable properties are properties that can themselves be serialized.
      This includes lists of items (i.e. the 'body' field of the adaptive card)
      or single objects that also inherit from Serializable
    """

    def __init__(self, serializable_properties, simple_properties):
        """
        Initialize a serializable object.

        Args:
            serializable_properties(list): List of all serializable properties
            simple_properties(list): List of all simple properties.
        """
        self.serializable_properties = serializable_properties
        self.simple_properties = simple_properties

    def to_dict(self):
        """
        Serialize the element into a Python dictionary.

        The to_dict() method recursively serializes the object's data into
        a Python dictionary.

        Returns:
            dict: Dictionary representation of this element.
        """
        serialized_data = {}
        for property_name in self.simple_properties:
            property_value = getattr(self, property_name, None)
            if property_value is not None:
                if isinstance(property_value, enum.Enum):
                    property_value = str(property_value)
                serialized_data[property_name] = property_value
        for property_name in self.serializable_properties:
            property_value = getattr(self, property_name, None)
            if property_value is not None:
                if isinstance(property_value, list):
                    serialized_data[property_name] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in property_value]
                else:
                    serialized_data[property_name] = property_value.to_dict()
        return serialized_data

    def to_json(self, **kwargs):
        """
        Serialize the element into JSON text.

        Any keyword arguments provided are passed through the Python JSON
        encoder.
        """
        return json.dumps(self.to_dict(), **kwargs)