
from __future__ import annotations

import json
from enum import Enum
from typing import Any, Dict, List, Optional


class EntityCategory(Enum):
    """Simple enumeration of possible entity categories."""

    DEVICE = "device"
    LOCATION = "location"
    METRIC = "metric"
    UNKNOWN = "unknown"


class AttributeManager:
    """Manager for entity attributes."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the attribute manager."""
        self.config = config

    def prepare_attributes(
        self,
        topic: str,
        category: str,
        parts: List[str],
        metric_info: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Prepare entity attributes."""
        attrs: Dict[str, Any] = {
            "topic": topic,
            "category": category,
            "parts": parts,
            "metric_info": metric_info or {},
        }
        entity_category = self.determine_entity_category(category)
        if entity_category is not None:
            attrs["entity_category"] = entity_category.value
        return attrs

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Process JSON payload to extract additional attributes."""
        try:
            data = json.loads(payload)
        except (json.JSONDecodeError, TypeError):
            return attributes

        if isinstance(data, dict):
            # Merge payload data into attributes, overriding existing keys
            merged = {**attributes, **data}
            return merged
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """Determine EntityCategory from attribute category."""
        for enum_val in EntityCategory:
            if enum_val.value == category.lower():
                return enum_val
        return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Extract and prepare GPS-related attributes."""
        gps_data: Dict[str, Any] = {}

        # Payload may be a dict or a JSON string
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                return gps_data

        if not isinstance(payload, dict):
            return gps_data

        # Common GPS keys
        gps_keys = ("latitude", "longitude", "altitude", "timestamp")
        # If payload contains a nested 'gps' dict, use that
        if "gps" in payload and isinstance(payload["gps"], dict):
            source = payload["gps"]
        else:
            source = payload

        for key in gps_keys:
            if key in source:
                gps_data[key] = source[key]

        # Add topic if provided
        if topic:
            gps_data["topic"] = topic

        return gps_data
