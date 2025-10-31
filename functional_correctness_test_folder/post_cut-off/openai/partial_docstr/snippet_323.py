
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class EntityCategory(Enum):
    """Enumeration of possible entity categories."""
    DEVICE = "device"
    SENSOR = "sensor"
    LOCATION = "location"
    METRIC = "metric"
    UNKNOWN = "unknown"


@dataclass
class AttributeManager:
    """Manages attributes for entities based on configuration and payload data."""

    config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Ensure config contains expected keys; provide defaults if missing
        self.config.setdefault("default_category", "unknown")
        self.config.setdefault(
            "gps_keys", {"lat": "latitude", "lon": "longitude", "alt": "altitude"})

    def prepare_attributes(
        self,
        topic: str,
        category: str,
        parts: List[str],
        metric_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Prepare a base set of attributes for an entity.

        Parameters
        ----------
        topic : str
            The topic string from which the entity originates.
        category : str
            The category string (e.g., 'device', 'sensor').
        parts : List[str]
            Additional parts of the topic or entity name.
        metric_info : Optional[Dict[str, Any]]
            Optional metric information to include.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the prepared attributes.
        """
        attrs: Dict[str, Any] = {
            "topic": topic,
            "category": category,
            "parts": parts,
        }
        if metric_info:
            attrs["metric_info"] = metric_info
        return attrs

    def process_json_payload(
        self, payload: str, attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse a JSON payload string and merge its contents into the existing attributes.

        Parameters
        ----------
        payload : str
            JSON string containing additional attributes.
        attributes : Dict[str, Any]
            Existing attributes to be updated.

        Returns
        -------
        Dict[str, Any]
            Updated attributes dictionary.
        """
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            # If payload is not valid JSON, return attributes unchanged
            return attributes

        if isinstance(data, dict):
            # Merge keys, giving precedence to payload values
            attributes.update(data)
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """
        Convert a category string into an EntityCategory enum member.

        Parameters
        ----------
        category : str
            Category string to be converted.

        Returns
        -------
        Optional[EntityCategory]
            The corresponding EntityCategory enum member, or None if unknown.
        """
        for enum_member in EntityCategory:
            if enum_member.value == category.lower():
                return enum_member
        return None

    def get_gps_attributes(
        self, topic: str, payload: Union[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Extract GPS-related attributes from a payload.

        Parameters
        ----------
        topic : str
            Topic string (used only for logging or future extensions).
        payload : Union[str, Dict[str, Any]]
            Payload containing GPS data; can be a JSON string or a dict.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing GPS attributes (latitude, longitude, altitude, timestamp).
        """
        gps_keys = self.config.get("gps_keys", {})
        gps_attrs: Dict[str, Any] = {}

        # Parse payload if it's a string
        if isinstance(payload, str):
            try:
                payload_data = json.loads(payload)
            except json.JSONDecodeError:
                return gps_attrs
        else:
            payload_data = payload

        if not isinstance(payload_data, dict):
            return gps_attrs

        # Extract latitude and longitude
        lat_key = gps_keys.get("lat", "latitude")
        lon_key = gps_keys.get("lon", "longitude")
        alt_key = gps_keys.get("alt", "altitude")

        if lat_key in payload_data and lon_key in payload_data:
            gps_attrs["latitude"] = payload_data[lat_key]
            gps_attrs["longitude"] = payload_data[lon_key]

        if alt_key in payload_data:
            gps_attrs["altitude"] = payload_data[alt_key]

        # Optional timestamp
        if "timestamp" in payload_data:
            gps_attrs["timestamp"] = payload_data["timestamp"]

        return gps_attrs
