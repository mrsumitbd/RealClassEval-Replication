
from typing import Dict, Any, List, Optional
from enum import Enum


class EntityCategory(Enum):
    LOCATION = 'location'
    SENSOR = 'sensor'
    DEVICE = 'device'


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
        import json
        try:
            json_data = json.loads(payload)
            attributes.update(json_data)
        except json.JSONDecodeError:
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        '''Determine EntityCategory from attribute category.'''
        try:
            return EntityCategory(category)
        except ValueError:
            return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        '''Extract and prepare GPS-related attributes.'''
        gps_attributes = {}
        if isinstance(payload, dict):
            gps_attributes = {k: v for k, v in payload.items(
            ) if k in ['latitude', 'longitude', 'altitude']}
        return gps_attributes
