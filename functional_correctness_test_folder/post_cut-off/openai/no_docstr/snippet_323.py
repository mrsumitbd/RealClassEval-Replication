
from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class EntityCategory(Enum):
    """Simple enumeration for entity categories."""
    DEVICE = "device"
    SENSOR = "sensor"
    LOCATION = "location"
    UNKNOWN = "unknown"


@dataclass
class AttributeManager:
    """
    Manage attributes for topics and payloads.

    Parameters
    ----------
    config : Dict[str, Any]
        Configuration dictionary that may contain mappings for
        category to EntityCategory and other defaults.
    """

    config: Dict[str, Any]

    def __post_init__(self) -> None:
        # Ensure config is a dict
        if not isinstance(self.config, dict):
            raise TypeError("config must be a dictionary")

    def prepare_attributes(
        self,
        topic: str,
        category: str,
        parts: List[str],
        metric_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Prepare a base attribute dictionary from topic, category, parts and optional metric info.

        Parameters
        ----------
        topic : str
            The topic string.
        category : str
            The category string.
        parts : List[str]
            List of parts derived from the topic.
        metric_info : Optional[Dict[str, Any]]
            Optional metric information to include.

        Returns
        -------
        Dict[str, Any]
            A dictionary of attributes.
        """
        attrs: Dict[str, Any] = {
            "topic": topic,
            "category": category,
            "parts": parts,
        }

        # Add metric info if provided
        if metric_info:
            attrs["metric"] = metric_info

        # Merge any defaults from config
        defaults = self.config.get("default_attributes", {})
        if isinstance(defaults, dict):
            attrs.update(defaults)

        return attrs

    def process_json_payload(
        self, payload: str, attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse a JSON payload string and merge it with existing attributes.

        Parameters
        ----------
        payload : str
            JSON string payload.
        attributes : Dict[str, Any]
            Existing attributes to merge with.

        Returns
        -------
        Dict[str, Any]
            Combined dictionary of attributes and payload data.
        """
        try:
            payload_dict = json.loads(payload)
            if not isinstance(payload_dict, dict):
                raise ValueError("Payload JSON must represent an object")
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON payload: {exc}") from exc

        # Merge payload into attributes; payload keys override existing ones
        combined = {**attributes, **payload_dict}
        return combined

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """
        Determine the EntityCategory enum value for a given category string.

        Parameters
        ----------
        category : str
            Category string to map.

        Returns
        -------
        Optional[EntityCategory]
            The corresponding EntityCategory or None if not found.
        """
        # First, try a direct mapping from config
        mapping = self.config.get("category_mapping", {})
        if isinstance(mapping, dict):
            enum_val = mapping.get(category.lower())
            if isinstance(enum_val, EntityCategory):
                return enum_val
            if isinstance(enum_val, str):
                try:
                    return EntityCategory(enum_val.lower())
                except ValueError:
                    pass

        # Fallback: try to match enum names
        try:
            return EntityCategory(category.lower())
        except ValueError:
            return None

    def get_gps_attributes(
        self, topic: str, payload: Union[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Extract GPS-related attributes from a payload.

        Parameters
        ----------
        topic : str
            The topic string (unused but kept for API compatibility).
        payload : Union[str, Dict[str, Any]]
            Payload that may contain GPS data. Can be a JSON string or a dict.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing 'latitude', 'longitude', and optionally 'altitude'.
        """
        # Parse payload if it's a string
        if isinstance(payload, str):
            try:
                payload_dict = json.loads(payload)
                if not isinstance(payload_dict, dict):
                    raise ValueError
            except Exception:
                raise ValueError("Payload must be a JSON object or dict")
        elif isinstance(payload, dict):
            payload_dict = payload
        else:
            raise TypeError("payload must be a dict or JSON string")

        gps_keys = ("latitude", "longitude", "altitude")
        gps_attrs: Dict[str, Any] = {}

        for key in gps_keys:
            if key in payload_dict:
                gps_attrs[key] = payload_dict[key]

        if "latitude" not in gps_attrs or "longitude" not in gps_attrs:
            raise ValueError(
                "Payload must contain at least latitude and longitude")

        return gps_attrs
