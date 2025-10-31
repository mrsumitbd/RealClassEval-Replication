
from typing import Dict, Any, List, Optional
from enum import Enum


class EntityCategory(Enum):
    LOCATION = 'location'
    DEVICE = 'device'
    EVENT = 'event'


class AttributeManager:

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        attributes = {
            'topic': topic,
            'category': category,
            'parts': parts
        }
        if metric_info:
            attributes.update(metric_info)
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        import json
        data = json.loads(payload)
        data.update(attributes)
        return data

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        try:
            return EntityCategory(category.upper())
        except ValueError:
            return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        if isinstance(payload, dict) and 'gps' in payload:
            return {
                'topic': topic,
                'latitude': payload['gps'].get('latitude'),
                'longitude': payload['gps'].get('longitude')
            }
        return {}
