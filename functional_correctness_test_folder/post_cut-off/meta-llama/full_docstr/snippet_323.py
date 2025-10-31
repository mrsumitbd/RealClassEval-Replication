
import json
from typing import Dict, Any, List, Optional


class EntityCategory:
    # Assuming EntityCategory is an Enum, if not, replace with the actual class
    def __init__(self, value):
        self.value = value


class AttributeManager:
    '''Manager for entity attributes.'''

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
        try:
            json_payload = json.loads(payload)
            attributes.update(json_payload)
        except json.JSONDecodeError:
            # Handle JSON decoding error
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        '''Determine EntityCategory from attribute category.'''
        # Assuming a simple mapping for demonstration purposes
        category_mapping = {
            'category1': EntityCategory('category1'),
            'category2': EntityCategory('category2')
        }
        return category_mapping.get(category)

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        '''Extract and prepare GPS-related attributes.'''
        gps_attributes = {}
        if isinstance(payload, dict) and 'latitude' in payload and 'longitude' in payload:
            gps_attributes['latitude'] = payload['latitude']
            gps_attributes['longitude'] = payload['longitude']
        return gps_attributes


# Example usage
if __name__ == "__main__":
    config = {
        'key': 'value'
    }
    attribute_manager = AttributeManager(config)

    topic = 'example_topic'
    category = 'category1'
    parts = ['part1', 'part2']
    metric_info = {
        'metric1': 'value1',
        'metric2': 'value2'
    }

    attributes = attribute_manager.prepare_attributes(
        topic, category, parts, metric_info)
    print(attributes)

    payload = '{"key": "value"}'
    updated_attributes = attribute_manager.process_json_payload(
        payload, attributes)
    print(updated_attributes)

    entity_category = attribute_manager.determine_entity_category(category)
    print(entity_category.value if entity_category else None)

    gps_payload = {
        'latitude': 37.7749,
        'longitude': -122.4194
    }
    gps_attributes = attribute_manager.get_gps_attributes(topic, gps_payload)
    print(gps_attributes)
