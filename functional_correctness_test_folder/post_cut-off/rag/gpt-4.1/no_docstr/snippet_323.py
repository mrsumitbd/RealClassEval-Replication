import json
from typing import Any, Dict, List, Optional


class EntityCategory:
    # Placeholder for actual EntityCategory implementation
    # In real code, this would be an Enum or similar
    CONFIG = "config"
    DIAGNOSTIC = "diagnostic"
    SYSTEM = "system"
    NONE = None

    @classmethod
    def from_str(cls, value: str):
        v = value.lower()
        if v == "config":
            return cls.CONFIG
        elif v == "diagnostic":
            return cls.DIAGNOSTIC
        elif v == "system":
            return cls.SYSTEM
        else:
            return cls.NONE


class AttributeManager:
    '''Manager for entity attributes.'''

    def __init__(self, config: Dict[str, Any]):
        '''Initialize the attribute manager.'''
        self._config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        '''Prepare entity attributes.'''
        attributes = {
            "topic": topic,
            "category": category,
            "parts": parts,
        }
        if metric_info:
            attributes.update(metric_info)
        # Optionally add config defaults
        if "defaults" in self._config:
            attributes.update(self._config["defaults"])
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        '''Process JSON payload to extract additional attributes.'''
        try:
            data = json.loads(payload)
            if isinstance(data, dict):
                attributes = attributes.copy()
                attributes.update(data)
        except Exception:
            # Ignore JSON errors, return attributes as is
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        '''Determine EntityCategory from attribute category.'''
        return EntityCategory.from_str(category)

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        '''Extract and prepare GPS-related attributes.'''
        gps_attrs = {}
        if isinstance(payload, str):
            try:
                data = json.loads(payload)
            except Exception:
                data = {}
        elif isinstance(payload, dict):
            data = payload
        else:
            data = {}

        for key in ("latitude", "longitude", "altitude", "accuracy"):
            if key in data:
                gps_attrs[key] = data[key]
        gps_attrs["topic"] = topic
        gps_attrs["type"] = "gps"
        return gps_attrs
