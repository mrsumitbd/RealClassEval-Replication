
from typing import Dict, Any, List, Optional
from enum import Enum
import json


class EntityCategory(Enum):
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    DEVICE = "device"
    OTHER = "other"


class AttributeManager:

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        attributes = {
            "topic": topic,
            "category": category,
            "parts": parts,
        }
        if metric_info:
            attributes.update(metric_info)
        if "defaults" in self.config:
            for k, v in self.config["defaults"].items():
                attributes.setdefault(k, v)
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        try:
            data = json.loads(payload)
            if isinstance(data, dict):
                attributes.update(data)
            else:
                attributes["payload"] = data
        except Exception:
            attributes["payload"] = payload
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        mapping = {
            "sensor": EntityCategory.SENSOR,
            "actuator": EntityCategory.ACTUATOR,
            "device": EntityCategory.DEVICE,
            "other": EntityCategory.OTHER,
        }
        return mapping.get(category.lower())

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        gps_attrs = {}
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                return gps_attrs
        if isinstance(payload, dict):
            lat = payload.get("latitude") or payload.get("lat")
            lon = payload.get("longitude") or payload.get(
                "lon") or payload.get("lng")
            alt = payload.get("altitude") or payload.get("alt")
            if lat is not None and lon is not None:
                gps_attrs["latitude"] = lat
                gps_attrs["longitude"] = lon
                if alt is not None:
                    gps_attrs["altitude"] = alt
        return gps_attrs
