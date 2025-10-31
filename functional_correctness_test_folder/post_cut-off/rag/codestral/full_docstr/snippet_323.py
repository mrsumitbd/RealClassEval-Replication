
from typing import Dict, Any, List, Optional
from enum import Enum


class EntityCategory(Enum):
    GPS = "gps"
    OTHER = "other"


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
            payload_data = json.loads(payload)
            attributes.update(payload_data)
        except json.JSONDecodeError:
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        '''Determine EntityCategory from attribute category.'''
        try:
            return EntityCategory(category.lower())
        except ValueError:
            return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        '''Extract and prepare GPS-related attributes.'''
        attributes = {
            'topic': topic,
            'category': 'gps'
        }
        if isinstance(payload, dict):
            attributes.update({
                'latitude': payload.get('latitude'),
                'longitude': payload.get('longitude'),
                'altitude': payload.get('altitude'),
                'speed': payload.get('speed'),
                'timestamp': payload.get('timestamp')
            })
        return attributes
