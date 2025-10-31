
from typing import Dict, Any, List, Optional
from enum import Enum


class EntityCategory(Enum):
    """Enum for entity categories."""
    CONFIG = "config"
    DIAGNOSTIC = "diagnostic"


class AttributeManager:
    """Manager for entity attributes."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the attribute manager."""
        self._config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        """Prepare entity attributes."""
        attributes: Dict[str, Any] = {
            "topic": topic,
            "category": category,
            "parts": parts,
        }
        if metric_info:
            attributes.update(metric_info)
        entity_category = self.determine_entity_category(category)
        if entity_category:
            attributes["entity_category"] = entity_category.value
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Process JSON payload to extract additional attributes."""
        try:
            import json
            payload_dict = json.loads(payload)
            if isinstance(payload_dict, dict):
                attributes.update(payload_dict)
        except (json.JSONDecodeError, TypeError):
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """Determine EntityCategory from attribute category."""
        if category.lower() in ("config", "configuration"):
            return EntityCategory.CONFIG
        elif category.lower() in ("diagnostic", "diagnostics"):
            return EntityCategory.DIAGNOSTIC
        return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Extract and prepare GPS-related attributes."""
        gps_attributes: Dict[str, Any] = {"topic": topic}
        if isinstance(payload, dict):
            for key in ["latitude", "longitude", "altitude", "speed", "bearing"]:
                if key in payload:
                    gps_attributes[key] = payload[key]
        return gps_attributes
