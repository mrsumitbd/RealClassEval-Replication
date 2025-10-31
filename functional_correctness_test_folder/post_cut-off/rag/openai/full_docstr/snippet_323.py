
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class EntityCategory(Enum):
    """Simple enumeration of possible entity categories."""
    DEVICE = "device"
    SENSOR = "sensor"
    LOCATION = "location"
    UNKNOWN = "unknown"


@dataclass
class AttributeManager:
    """Manager for entity attributes."""

    config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Ensure config is a dict
        if not isinstance(self.config, dict):
            raise TypeError("config must be a dict")

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
        }
        if metric_info:
            attrs["metric_info"] = metric_info
        return attrs

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Process JSON payload to extract additional attributes."""
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            # If payload is not valid JSON, return attributes unchanged
            return attributes

        if isinstance(data, dict):
            # Merge payload dict into attributes, overriding existing keys
            merged = {**attributes, **data}
            return merged
        # If payload is not a dict, ignore it
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """Determine EntityCategory from attribute category."""
        mapping = {
            "device": EntityCategory.DEVICE,
            "sensor": EntityCategory.SENSOR,
            "location": EntityCategory.LOCATION,
        }
        return mapping.get(category.lower())

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Extract and prepare GPS-related attributes."""
        attrs: Dict[str, Any] = {"topic": topic}

        # Accept payload as dict or JSON string
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                return attrs

        if not isinstance(payload, dict):
            return attrs

        # Common GPS keys
        gps_keys = ["latitude", "longitude",
                    "altitude", "timestamp", "accuracy"]
        for key in gps_keys:
            if key in payload:
                attrs[key] = payload[key]

        return attrs
