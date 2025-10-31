
from typing import Dict, Any, List, Optional
import json
from enum import Enum


class EntityCategory(Enum):
    CONFIG = "config"
    DIAGNOSTIC = "diagnostic"
    SYSTEM = "system"
    NONE = "none"


class AttributeManager:

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
        except Exception:
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        '''Determine EntityCategory from attribute category.'''
        mapping = {
            "config": EntityCategory.CONFIG,
            "diagnostic": EntityCategory.DIAGNOSTIC,
            "system": EntityCategory.SYSTEM,
            "none": EntityCategory.NONE,
        }
        return mapping.get(category.lower(), None)

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        '''Extract and prepare GPS-related attributes.'''
        gps_attrs = {}
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                return gps_attrs
        if isinstance(payload, dict):
            lat = payload.get("latitude") or payload.get("lat")
            lon = payload.get("longitude") or payload.get("lon")
            alt = payload.get("altitude") or payload.get("alt")
            if lat is not None and lon is not None:
                gps_attrs["latitude"] = lat
                gps_attrs["longitude"] = lon
                if alt is not None:
                    gps_attrs["altitude"] = alt
        return gps_attrs
