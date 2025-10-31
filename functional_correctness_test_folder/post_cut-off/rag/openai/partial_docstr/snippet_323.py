
from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class EntityCategory(Enum):
    """Simple enumeration of possible entity categories."""

    DEVICE = "device"
    LOCATION = "location"
    METRIC = "metric"
    UNKNOWN = "unknown"


@dataclass
class AttributeManager:
    """Manager for entity attributes."""

    config: Dict[str, Any]

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
        separator = self.config.get("entity_separator", "_")
        entity_id = separator.join(parts)

        attributes: Dict[str, Any] = {
            "topic": topic,
            "category": category,
            "parts": parts,
            "entity_id": entity_id,
        }
        if metric_info is not None:
            attributes["metric_info"] = metric_info
        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Process JSON payload to extract additional attributes."""
        try:
            data = json.loads(payload)
        except (json.JSONDecodeError, TypeError):
            # If payload is not a valid JSON string, return attributes unchanged
            return attributes

        if isinstance(data, dict):
            # Merge JSON data into attributes, overriding existing keys if necessary
            merged = {**attributes, **data}
            return merged
        # If payload is not a dict, ignore it
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """Determine EntityCategory from attribute category."""
        for enum_val in EntityCategory:
            if enum_val.value == category.lower():
                return enum_val
        return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Extract and prepare GPS-related attributes."""
        gps_attrs: Dict[str, Any] = {"topic": topic}

        # Helper to extract lat/lon from a dict
        def _extract_from_dict(d: Dict[str, Any]) -> Optional[Dict[str, Any]]:
            lat = d.get("latitude") or d.get("lat")
            lon = d.get("longitude") or d.get("lon")
            if lat is not None and lon is not None:
                attrs: Dict[str, Any] = {"latitude": lat, "longitude": lon}
                if "altitude" in d:
                    attrs["altitude"] = d["altitude"]
                return attrs
            return None

        if isinstance(payload, dict):
            # Direct GPS fields
            gps_attrs.update(_extract_from_dict(payload) or {})
            # Nested GPS dict
            if "gps" in payload and isinstance(payload["gps"], dict):
                gps_attrs.update(_extract_from_dict(payload["gps"]) or {})
        elif isinstance(payload, list):
            # Search each element for GPS data
            for item in payload:
                if isinstance(item, dict):
                    extracted = _extract_from_dict(item)
                    if extracted:
                        gps_attrs.update(extracted)
                        break

        return gps_attrs
