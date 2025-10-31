from typing import Any, Dict, List, Optional
import json
from datetime import datetime, timezone

try:
    from homeassistant.helpers.entity import EntityCategory  # type: ignore
except Exception:
    from enum import Enum

    class EntityCategory(Enum):  # type: ignore
        CONFIG = "config"
        DIAGNOSTIC = "diagnostic"


class AttributeManager:
    """Manager for entity attributes."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the attribute manager."""
        self._config = config or {}
        self._category_map = {
            "config": EntityCategory.CONFIG,
            "configuration": EntityCategory.CONFIG,
            "diagnostic": EntityCategory.DIAGNOSTIC,
            "diagnostics": EntityCategory.DIAGNOSTIC,
        }

        default_gps_keys = {
            "latitude": ["latitude", "lat", "Lat", "Latitude", "y"],
            "longitude": ["longitude", "lon", "lng", "Lon", "Longitude", "x"],
            "accuracy": ["gps_accuracy", "accuracy", "acc", "hacc", "hdop"],
            "altitude": ["altitude", "alt", "elevation"],
            "speed": ["speed", "vel", "velocity"],
            "heading": ["heading", "course", "bearing", "dir"],
            "timestamp": ["timestamp", "ts", "time", "datetime", "date"],
        }
        self._gps_keys = self._config.get("gps_keys", default_gps_keys)
        self._gps_nested_paths = self._config.get(
            "gps_nested_paths", ["gps", "location", "coords", "position"]
        )

    def prepare_attributes(
        self,
        topic: str,
        category: str,
        parts: List[str],
        metric_info: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Prepare entity attributes."""
        attrs: Dict[str, Any] = {}
        attrs["topic"] = topic
        attrs["category"] = category
        entity_category = self.determine_entity_category(category)
        if entity_category is not None:
            attrs["entity_category"] = entity_category

        name = self._config.get("name")
        if not name:
            if parts:
                last = parts[-1]
                name = last.replace("_", " ").replace("-", " ").strip().title()
            else:
                name = topic.split("/")[-1].replace("_",
                                                    " ").replace("-", " ").strip().title()
        if name:
            attrs["name"] = name

        object_id = self._config.get("object_id")
        if not object_id:
            object_id = "_".join([p for p in parts if p]
                                 ) or topic.replace("/", "_")
        attrs["object_id"] = object_id

        if isinstance(metric_info, dict):
            for k, v in metric_info.items():
                attrs[k] = v

        return attrs

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Process JSON payload to extract additional attributes."""
        if not isinstance(payload, str):
            return attributes
        try:
            data = json.loads(payload)
        except Exception:
            return attributes

        if not isinstance(data, dict):
            return attributes

        extras: Dict[str, Any] = {}
        for k, v in data.items():
            if isinstance(v, (str, int, float, bool)) or v is None:
                extras[k] = v

        gps = self.get_gps_attributes(attributes.get("topic", ""), data)
        extras.update(gps)

        existing = attributes.get("extra_attributes")
        if not isinstance(existing, dict):
            attributes["extra_attributes"] = extras
        else:
            existing.update(extras)
            attributes["extra_attributes"] = existing

        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """Determine EntityCategory from attribute category."""
        if not isinstance(category, str) or not category:
            return None
        key = category.strip().lower()
        return self._category_map.get(key)

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Extract and prepare GPS-related attributes."""
        data: Optional[Dict[str, Any]] = None
        if isinstance(payload, dict):
            data = payload
        elif isinstance(payload, str):
            try:
                obj = json.loads(payload)
                if isinstance(obj, dict):
                    data = obj
            except Exception:
                data = None

        if not data:
            return {}

        def _first_present(d: Dict[str, Any], keys: List[str]) -> Optional[Any]:
            for k in keys:
                if k in d:
                    return d[k]
            return None

        def _search_nested(d: Dict[str, Any], nested_keys: List[str]) -> Dict[str, Any]:
            out: Dict[str, Any] = {}
            cand = {}
            for nk in nested_keys:
                if nk in d and isinstance(d[nk], dict):
                    cand = d[nk]
                    break
            if cand:
                out.update(cand)
            return out

        base = dict(data)
        nested = _search_nested(data, self._gps_nested_paths)
        merged = {**base, **nested}

        lat = _first_present(merged, self._gps_keys.get("latitude", []))
        lon = _first_present(merged, self._gps_keys.get("longitude", []))
        acc = _first_present(merged, self._gps_keys.get("accuracy", []))
        alt = _first_present(merged, self._gps_keys.get("altitude", []))
        spd = _first_present(merged, self._gps_keys.get("speed", []))
        hdg = _first_present(merged, self._gps_keys.get("heading", []))
        ts = _first_present(merged, self._gps_keys.get("timestamp", []))

        gps_attrs: Dict[str, Any] = {}

        if lat is not None and lon is not None:
            try:
                gps_attrs["latitude"] = float(lat)
                gps_attrs["longitude"] = float(lon)
            except Exception:
                pass

        if acc is not None:
            try:
                gps_attrs["gps_accuracy"] = float(acc)
            except Exception:
                try:
                    gps_attrs["gps_accuracy"] = int(acc)
                except Exception:
                    pass

        if alt is not None:
            try:
                gps_attrs["altitude"] = float(alt)
            except Exception:
                try:
                    gps_attrs["altitude"] = int(alt)
                except Exception:
                    pass

        if spd is not None:
            try:
                gps_attrs["speed"] = float(spd)
            except Exception:
                try:
                    gps_attrs["speed"] = int(spd)
                except Exception:
                    pass

        if hdg is not None:
            try:
                gps_attrs["heading"] = float(hdg)
            except Exception:
                try:
                    gps_attrs["heading"] = int(hdg)
                except Exception:
                    pass

        if ts is not None:
            iso = self._parse_timestamp(ts)
            if iso:
                gps_attrs["timestamp"] = iso

        return gps_attrs

    @staticmethod
    def _parse_timestamp(value: Any) -> Optional[str]:
        if value is None:
            return None
        # numeric epoch seconds or milliseconds
        if isinstance(value, (int, float)):
            try:
                v = float(value)
                if v > 1e12:
                    v = v / 1000.0
                dt = datetime.fromtimestamp(v, tz=timezone.utc)
                return dt.isoformat().replace("+00:00", "Z")
            except Exception:
                return None
        # string ISO or epoch string
        if isinstance(value, str):
            s = value.strip()
            if not s:
                return None
            if s.isdigit():
                try:
                    v = float(s)
                    if v > 1e12:
                        v = v / 1000.0
                    dt = datetime.fromtimestamp(v, tz=timezone.utc)
                    return dt.isoformat().replace("+00:00", "Z")
                except Exception:
                    return None
            try:
                # Handle trailing Z
                if s.endswith("Z"):
                    s = s[:-1] + "+00:00"
                dt = datetime.fromisoformat(s)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                else:
                    dt = dt.astimezone(timezone.utc)
                return dt.isoformat().replace("+00:00", "Z")
            except Exception:
                return None
        return None
