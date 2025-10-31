
from typing import Dict, Any, List, Optional
import json
from enum import Enum


class EntityCategory(Enum):
    DIAGNOSTIC = "diagnostic"
    CONFIG = "config"


class AttributeManager:

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        attributes = {
            "topic": topic,
            "category": category,
            "parts": parts
        }
        if metric_info:
            attributes.update(metric_info)
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        try:
            payload_dict = json.loads(payload)
            attributes["payload"] = payload_dict
        except json.JSONDecodeError:
            attributes["payload"] = payload
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        if category.lower() == "diagnostic":
            return EntityCategory.DIAGNOSTIC
        elif category.lower() == "config":
            return EntityCategory.CONFIG
        return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        gps_attributes = {
            "topic": topic,
            "latitude": payload.get("lat"),
            "longitude": payload.get("lon"),
            "altitude": payload.get("alt"),
            "timestamp": payload.get("timestamp")
        }
        return gps_attributes
