
from typing import Dict, Any, List, Optional
import json
from enum import Enum


class EntityCategory(Enum):
    DIAGNOSTIC = "diagnostic"
    CONFIG = "config"


class AttributeManager:
    '''Manager for entity attributes.'''

    def __init__(self, config: Dict[str, Any]):
        '''Initialize the attribute manager.'''
        self.config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        '''Prepare entity attributes.'''
        attributes = {
            "topic": topic,
            "category": category,
            "parts": parts,
        }
        if metric_info:
            attributes.update(metric_info)
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        '''Process JSON payload to extract additional attributes.'''
        try:
            data = json.loads(payload)
            if isinstance(data, dict):
                attributes.update(data)
        except json.JSONDecodeError:
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        '''Determine EntityCategory from attribute category.'''
        if category == "diagnostic":
            return EntityCategory.DIAGNOSTIC
        elif category == "config":
            return EntityCategory.CONFIG
        return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        '''Extract and prepare GPS-related attributes.'''
        attributes = {"topic": topic}
        if isinstance(payload, dict):
            if "latitude" in payload and "longitude" in payload:
                attributes["latitude"] = payload["latitude"]
                attributes["longitude"] = payload["longitude"]
            if "altitude" in payload:
                attributes["altitude"] = payload["altitude"]
        return attributes
