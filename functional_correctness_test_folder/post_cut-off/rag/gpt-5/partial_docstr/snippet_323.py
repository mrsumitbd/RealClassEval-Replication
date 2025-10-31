from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

try:
    # Prefer Home Assistant's EntityCategory if available for compatibility
    from homeassistant.helpers.entity import EntityCategory as _HAEntityCategory  # type: ignore

    EntityCategory = _HAEntityCategory  # type: ignore
except Exception:  # pragma: no cover
    from enum import Enum

    class EntityCategory(Enum):
        CONFIG = "config"
        DIAGNOSTIC = "diagnostic"


_LOGGER = logging.getLogger(__name__)


def _safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        s = str(value).strip()
        if not s:
            return None
        return float(s)
    except Exception:
        return None


def _safe_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    try:
        s = str(value).strip()
        if not s:
            return None
        return int(float(s))
    except Exception:
        return None


def _to_iso_timestamp(value: Any) -> Optional[str]:
    if value is None:
        return None
    # If it is already a datetime
    if isinstance(value, datetime):
        return value.replace(microsecond=0).isoformat()
    # Try numeric epoch seconds or millis
    if isinstance(value, (int, float)):
        try:
            # Detect millis vs seconds
            ts = float(value)
            if ts > 10_000_000_000:  # clearly millis
                ts = ts / 1000.0
            return datetime.utcfromtimestamp(ts).replace(microsecond=0).isoformat() + "Z"
        except Exception:
            pass
    # Try parse string
    try:
        s = str(value).strip()
        if not s:
            return None
        # If already iso-like, return as is
        # Minimal check
        if "T" in s or s.endswith("Z"):
            return s
        # Try as int/float string epoch
        if s.isdigit():
            return _to_iso_timestamp(int(s))
        try:
            f = float(s)
            return _to_iso_timestamp(f)
        except Exception:
            pass
        # Fallback: try common formats
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(s, fmt)
                return dt.replace(microsecond=0).isoformat()
            except Exception:
                continue
    except Exception:
        return None
    return None


@dataclass(frozen=True)
class _KeySpec:
    # Standardized attribute key the manager uses in outputs
    std_key: str
    # Optional converter to coerce data type
    conv: Optional[Any] = None


class AttributeManager:
    '''Manager for entity attributes.'''

    def __init__(self, config: Dict[str, Any]):
        '''Initialize the attribute manager.'''
        self._config = dict(
            config or {})  # shallow copy to avoid mutation side effects

        # Default attributes that will be merged into every prepared attribute dict
        self._defaults: Dict[str, Any] = dict(self._config.get("defaults", {}))

        # Optional device block that can be attached
        self._device: Dict[str, Any] = dict(self._config.get("device", {}))

        # Optional namespace to generate unique_id
        self._namespace: str = str(self._config.get("namespace", "entity"))

        # Mapping of string categories to entity categories
        self._category_map: Dict[str, EntityCategory] = {}
        raw_map = self._config.get("entity_category_map", {})
        if isinstance(raw_map, dict):
            for k, v in raw_map.items():
                if isinstance(v, EntityCategory):
                    self._category_map[str(k).lower()] = v
                elif isinstance(v, str):
                    vk = v.lower().strip()
                    if vk in ("config", "configuration", "setup"):
                        self._category_map[str(
                            k).lower()] = EntityCategory.CONFIG
                    elif vk in ("diagnostic", "diagnostics", "status", "debug", "meta"):
                        self._category_map[str(
                            k).lower()] = EntityCategory.DIAGNOSTIC

        # Mapping for JSON payload keys to standardized keys
        # Later keys override earlier if duplicates exist across synonyms
        self._json_attribute_map: Dict[str, _KeySpec] = {
            # Coordinates
            "lat": _KeySpec("latitude", _safe_float),
            "latitude": _KeySpec("latitude", _safe_float),
            "lon": _KeySpec("longitude", _safe_float),
            "lng": _KeySpec("longitude", _safe_float),
            "long": _KeySpec("longitude", _safe_float),
            "longitude": _KeySpec("longitude", _safe_float),
            # GPS accuracy / dilution
            "acc": _KeySpec("gps_accuracy", _safe_float),
            "accuracy": _KeySpec("gps_accuracy", _safe_float),
            "hdop": _KeySpec("hdop", _safe_float),
            "vdop": _KeySpec("vdop", _safe_float),
            "pdop": _KeySpec("pdop", _safe_float),
            # Altitude / speed / course
            "alt": _KeySpec("altitude", _safe_float),
            "altitude": _KeySpec("altitude", _safe_float),
            "vel": _KeySpec("speed", _safe_float),
            "speed": _KeySpec("speed", _safe_float),
            "course": _KeySpec("course", _safe_float),
            "bearing": _KeySpec("course", _safe_float),
            "dir": _KeySpec("course", _safe_float),
            # Satellites, fix
            "sat": _KeySpec("sats", _safe_int),
            "sats": _KeySpec("sats", _safe_int),
            "fix": _KeySpec("fix", _safe_int),
            # Battery, provider
            "bat": _KeySpec("battery", _safe_float),
            "battery": _KeySpec("battery", _safe_float),
            "provider": _KeySpec("provider", None),
            # Timestamp
            "timestamp": _KeySpec("timestamp", _to_iso_timestamp),
            "time": _KeySpec("timestamp", _to_iso_timestamp),
            "ts": _KeySpec("timestamp", _to_iso_timestamp),
        }

        # Allow user to extend/override the json attribute map via config
        user_map: Dict[str, Union[str, Dict[str, Any]]
                       ] = self._config.get("json_attribute_map", {}) or {}
        if isinstance(user_map, dict):
            for incoming_key, spec in user_map.items():
                if isinstance(spec, str):
                    self._json_attribute_map[incoming_key] = _KeySpec(
                        spec, None)
                elif isinstance(spec, dict):
                    std_key = spec.get("key") or spec.get("std_key")
                    conv = spec.get("conv")
                    if std_key:
                        self._json_attribute_map[incoming_key] = _KeySpec(
                            str(std_key), conv if callable(conv) else None)

        # Whether to store raw payloads inside attributes for debugging
        self._store_raw: bool = bool(
            self._config.get("store_raw_payload", False))

        # Name template if provided. Available placeholders: topic, category, last, parts, metric_name
        self._name_template: Optional[str] = self._config.get("name_template")

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        '''Prepare entity attributes.'''
        metric_info = metric_info or {}
        attributes: Dict[str, Any] = {}

        # Merge defaults first
        attributes.update(self._defaults)

        # Friendly name
        friendly_name: Optional[str] = None
        mi_name = metric_info.get("name")
        if isinstance(mi_name, str) and mi_name.strip():
            friendly_name = mi_name.strip()
        elif isinstance(self._name_template, str) and self._name_template:
            try:
                friendly_name = self._name_template.format(
                    topic=topic,
                    category=category,
                    last=(parts[-1] if parts else ""),
                    parts="_".join(parts),
                    metric_name=mi_name or "",
                )
            except Exception:
                friendly_name = None
        if not friendly_name:
            base = (parts[-1] if parts else category) or topic
            friendly_name = str(base).replace("_", " ").strip().title()
        attributes["friendly_name"] = friendly_name

        # Unique ID
        uid_bits = [self._namespace, topic or "", category or ""]
        if parts:
            uid_bits.extend(parts)
        attributes["unique_id"] = ":".join(
            [str(x) for x in uid_bits if str(x)]).lower()

        # Entity category
        cat = metric_info.get("entity_category")
        if isinstance(cat, EntityCategory):
            attributes["entity_category"] = cat
        elif isinstance(cat, str):
            attributes["entity_category"] = self.determine_entity_category(cat)
        else:
            attributes["entity_category"] = self.determine_entity_category(
                category)

        # Merge device info if present
        if self._device:
            attributes["device"] = self._device

        # Metric info passthrough
        for key in ("unit_of_measurement", "device_class", "state_class", "icon"):
            if key in metric_info and metric_info[key] is not None:
                attributes[key] = metric_info[key]

        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        '''Process JSON payload to extract additional attributes.'''
        merged = dict(attributes or {})
        try:
            data = json.loads(payload)
        except Exception as e:
            _LOGGER.debug("Failed to parse JSON payload: %s", e)
            if self._store_raw:
                merged["raw_payload"] = payload
            return merged

        flat = self._flatten_payload(data)

        # Map incoming keys to standardized attribute keys
        updates: Dict[str, Any] = {}
        for in_key, value in flat.items():
            key_lower = str(in_key).lower()
            spec = self._json_attribute_map.get(key_lower)
            if not spec:
                continue
            conv = spec.conv
            v = conv(value) if callable(conv) else value
            if v is None:
                continue
            # Avoid overriding existing with None or empty
            updates[spec.std_key] = v

        # Merge updates last to override defaults if necessary
        merged.update(updates)

        # Optional derived attribute: coordinates tuple if both lat/lon exist
        lat = merged.get("latitude")
        lon = merged.get("longitude")
        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
            merged["coordinates"] = (float(lat), float(lon))

        if self._store_raw:
            merged["raw_payload"] = data

        return merged

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        '''Determine EntityCategory from attribute category.'''
        if not category:
            return None
        cl = str(category).strip().lower()

        # Config-provided explicit mapping takes precedence
        if cl in self._category_map:
            return self._category_map[cl]

        # Built-in mapping
        if cl in ("config", "configuration", "setup"):
            return EntityCategory.CONFIG
        if cl in ("diagnostic", "diagnostics", "status", "debug", "meta"):
            return EntityCategory.DIAGNOSTIC
        return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        '''Extract and prepare GPS-related attributes.'''
        # Normalize payload to dict
        data: Dict[str, Any] = {}
        if isinstance(payload, str):
            try:
                data = json.loads(payload)
            except Exception:
                # Not JSON, cannot parse
                return {}
        elif isinstance(payload, dict):
            data = payload
        else:
            return {}

        flat = self._flatten_payload(data)

        attrs: Dict[str, Any] = {}

        # Extract using the same mapping as process_json_payload
        for in_key, value in flat.items():
            key_lower = str(in_key).lower()
            spec = self._json_attribute_map.get(key_lower)
            if not spec:
                continue
            if spec.std_key not in {
                "latitude",
                "longitude",
                "gps_accuracy",
                "altitude",
                "speed",
                "course",
                "sats",
                "fix",
                "timestamp",
                "provider",
                "battery",
                "hdop",
                "vdop",
                "pdop",
            }:
                continue
            conv = spec.conv
            v = conv(value) if callable(conv) else value
            if v is None:
                continue
            attrs[spec.std_key] = v

        # Derive coordinates tuple if possible
        lat = attrs.get("latitude")
        lon = attrs.get("longitude")
        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
            attrs["coordinates"] = (float(lat), float(lon))

        # Add topic context
        if topic:
            attrs["source_topic"] = topic

        return attrs

    def _flatten_payload(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten known nested structures commonly found in tracker payloads."""
        if not isinstance(data, dict):
            return {}

        result: Dict[str, Any] = dict(data)

        # Common nested keys we can flatten: position, gps, location, coords
        for key in ("position", "gps", "location", "coords"):
            nested = data.get(key)
            if isinstance(nested, dict):
                for k, v in nested.items():
                    if k not in result:
                        result[k] = v

        # Some providers use 'lat'/'lon' inside "geometry": {"coordinates":[lon, lat]}
        geometry = data.get("geometry")
        if isinstance(geometry, dict):
            coords = geometry.get("coordinates")
            if isinstance(coords, (list, tuple)) and len(coords) >= 2:
                lon, lat = coords[0], coords[1]
                if "lon" not in result and "longitude" not in result:
                    result["lon"] = lon
                if "lat" not in result and "latitude" not in result:
                    result["lat"] = lat

        # Traccar style "fixTime" or "deviceTime"
        for tkey in ("fixTime", "deviceTime", "serverTime"):
            if tkey in data and "timestamp" not in result and "time" not in result and "ts" not in result:
                result["timestamp"] = data[tkey]

        return result
