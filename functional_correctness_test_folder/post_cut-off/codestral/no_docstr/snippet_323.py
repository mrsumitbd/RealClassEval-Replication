
from typing import Dict, Any, List, Optional
from enum import Enum


class EntityCategory(Enum):
    GPS = "GPS"
    OTHER = "OTHER"


class AttributeManager:

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        attributes = {
            'topic': topic,
            'category': category,
            'parts': parts,
            'metric_info': metric_info if metric_info else {}
        }
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        import json
        try:
            payload_dict = json.loads(payload)
            attributes.update(payload_dict)
        except json.JSONDecodeError:
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        if category == "GPS":
            return EntityCategory.GPS
        else:
            return EntityCategory.OTHER

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        gps_attributes = {
            'topic': topic,
            'latitude': payload.get('latitude'),
            'longitude': payload.get('longitude'),
            'altitude': payload.get('altitude')
        }
        return gps_attributes
