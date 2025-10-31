
from typing import Dict, Any, List, Optional
import json
from enum import Enum


class EntityCategory(str, Enum):
    """Entity category enumeration."""
    CONFIG = 'config'
    DIAGNOSTIC = 'diagnostic'


class AttributeManager:
    """Manager for entity attributes."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the attribute manager."""
        self._config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        """Prepare entity attributes."""
        attributes = {
            'topic': topic,
            'category': category,
            'parts': parts
        }
        if metric_info:
            attributes.update(metric_info)
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Process JSON payload to extract additional attributes."""
        try:
            json_payload = json.loads(payload)
            attributes.update(json_payload)
        except json.JSONDecodeError:
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """Determine EntityCategory from attribute category."""
        try:
            return EntityCategory(category)
        except ValueError:
            return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Extract and prepare GPS-related attributes."""
        # Assuming GPS payload is in JSON format with 'latitude' and 'longitude' keys
        try:
            gps_data = json.loads(payload)
            attributes = self.prepare_attributes(topic, 'gps', ['location'])
            attributes['latitude'] = gps_data.get('latitude')
            attributes['longitude'] = gps_data.get('longitude')
            return attributes
        except json.JSONDecodeError:
            return {}
