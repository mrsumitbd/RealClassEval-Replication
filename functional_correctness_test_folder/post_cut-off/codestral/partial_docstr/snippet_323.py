
from typing import Dict, Any, List, Optional
from enum import Enum


class EntityCategory(Enum):
    VEHICLE = "vehicle"
    PERSON = "person"
    ANIMAL = "animal"
    OBJECT = "object"


class AttributeManager:

    def __init__(self, config: Dict[str, Any]):
        '''Initialize the attribute manager.'''
        self.config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        '''Prepare entity attributes.'''
        attributes = {
            'topic': topic,
            'category': category,
            'parts': parts,
            'metric_info': metric_info if metric_info else {}
        }
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        '''Process JSON payload to extract additional attributes.'''
        import json
        try:
            payload_dict = json.loads(payload)
            attributes.update(payload_dict)
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
        if hasattr(payload, 'latitude') and hasattr(payload, 'longitude'):
            gps_attributes['latitude'] = payload.latitude
            gps_attributes['longitude'] = payload.longitude
        return gps_attributes
