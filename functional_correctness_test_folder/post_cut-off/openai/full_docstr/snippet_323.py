
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class EntityCategory(Enum):
    VEHICLE = "vehicle"
    SENSOR = "sensor"
    UNKNOWN = "unknown"


@dataclass
class AttributeManager:
    """Manager for entity attributes."""

    config: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, config: Dict[str, Any]):
        """Initialize the attribute manager."""
        self.config = dict(config)  # shallow copy to avoid side‑effects

    def prepare_attributes(
        self,
        topic: str,
        category: str,
        parts: List[str],
        metric_info: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Prepare entity attributes."""
        attrs: Dict[str, Any] = dict(self.config)  # start with defaults
        attrs.update(
            {
                "topic": topic,
                "category": category,
                "parts": parts,
            }
        )
        if metric_info:
            attrs["metric_info"] = metric_info
        return attrs

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Process JSON payload to extract additional attributes."""
        try:
            data = json.loads(payload)
        except (json.JSONDecodeError, TypeError):
            # If payload is not a valid JSON string, return attributes unchanged
            return attributes

        # Merge payload data into attributes; payload keys override existing ones
        merged = dict(attributes)
        merged.update(data)
        return merged

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """Determine EntityCategory from attribute category."""
        mapping = {
            "vehicle": EntityCategory.VEHICLE,
            "sensor": EntityCategory.SENSOR,
        }
        return mapping.get(category.lower())

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Extract and prepare GPS-related attributes."""
        # Accept payload as dict or JSON string
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                return {}

        if not isinstance(payload, dict):
            return {}

        gps_keys = ["lat", "lon", "alt", "speed", "heading"]
        gps_attrs: Dict[str, Any] = {}
        for key in gps_keys:
            if key in payload:
                gps_attrs[key] = payload[key]

        # Include topic if provided
        if topic:
            gps_attrs["topic"] = topic

        return gps_attrs
