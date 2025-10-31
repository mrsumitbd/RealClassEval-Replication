
from typing import Dict, Any, List, Optional


class EntityCategory:
    # Assuming EntityCategory is an Enum, if not, replace with the actual class
    def __init__(self, value):
        self.value = value


class AttributeManager:

    def __init__(self, config: Dict[str, Any]):
        '''Initialize the attribute manager.'''
        self.config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        '''Prepare entity attributes.'''
        attributes = {
            'topic': topic,
            'category': category,
            'parts': parts
        }
        if metric_info:
            attributes.update(metric_info)
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        '''Process JSON payload to extract additional attributes.'''
        import json
        try:
            payload_dict = json.loads(payload)
            attributes.update(payload_dict)
        except json.JSONDecodeError:
            # Handle JSON decode error
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        '''Determine EntityCategory from attribute category.'''
        # Assuming a simple mapping for demonstration purposes
        category_mapping = {
            'sensor': EntityCategory('sensor'),
            'device': EntityCategory('device')
        }
        return category_mapping.get(category)

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        '''Extract and prepare GPS-related attributes.'''
        gps_attributes = {}
        # Assuming payload is a dictionary with 'latitude' and 'longitude' keys
        if isinstance(payload, dict) and 'latitude' in payload and 'longitude' in payload:
            gps_attributes['latitude'] = payload['latitude']
            gps_attributes['longitude'] = payload['longitude']
        return gps_attributes
