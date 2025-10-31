
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
            data = json.loads(payload)
            if isinstance(data, dict):
                attributes.update(data)
        except (json.JSONDecodeError, TypeError):
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """Determine EntityCategory from attribute category."""
        category_lower = category.lower()
        if category_lower == "config":
            return EntityCategory.CONFIG
        elif category_lower == "diagnostic":
            return EntityCategory.DIAGNOSTIC
        return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Extract and prepare GPS-related attributes."""
        gps_attributes: Dict[str, Any] = {"topic": topic}
        if isinstance(payload, dict):
            gps_data = payload.get("gps", {})
            if isinstance(gps_data, dict):
                gps_attributes.update({
                    "latitude": gps_data.get("latitude"),
                    "longitude": gps_data.get("longitude"),
                    "altitude": gps_data.get("altitude"),
                })
        return gps_attributes
