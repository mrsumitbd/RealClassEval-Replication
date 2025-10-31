from typing import Any, Dict, List, Optional
import json
from datetime import datetime


class AttributeManager:
    """Manager for entity attributes."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the attribute manager."""
        self._config: Dict[str, Any] = dict(config or {})

        gps_conf = self._config.get("gps", {}) if isinstance(
            self._config.get("gps"), dict) else {}

        # Known key variants for GPS data extraction
        self._gps_lat_keys: List[str] = gps_conf.get(
            "lat_keys", ["lat", "latitude"])
        self._gps_lon_keys: List[str] = gps_conf.get(
            "lon_keys", ["lon", "lng", "longitude", "long"])
        self._gps_acc_keys: List[str] = gps_conf.get(
            "accuracy_keys", ["acc", "accuracy", "hacc", "h_accuracy", "hdop"])
        self._gps_alt_keys: List[str] = gps_conf.get(
            "altitude_keys", ["alt", "altitude"])
        self._gps_spd_keys: List[str] = gps_conf.get(
            "speed_keys", ["spd", "speed", "velocity"])
        self._gps_brg_keys: List[str] = gps_conf.get(
            "bearing_keys", ["brg", "bearing", "course", "heading"])
        self._gps_ts_keys: List[str] = gps_conf.get(
            "timestamp_keys", ["ts", "time", "timestamp", "datetime", "dt"])

        # Optional JSON attributes inclusion list
        self._json_attributes: Optional[List[str]] = None
        if isinstance(self._config.get("json_attributes"), list):
            self._json_attributes = [str(k)
                                     for k in self._config["json_attributes"]]

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        """Prepare entity attributes."""
        attributes: Dict[str, Any] = {}

        # Include base attributes from configuration if provided
        base_attrs = self._config.get("attributes")
        if isinstance(base_attrs, dict):
            attributes.update(base_attrs)

        attributes["topic"] = topic
        attributes["topic_parts"] = list(parts)
        attributes["raw_category"] = category

        entity_category = self.determine_entity_category(category)
        if entity_category is not None:
            attributes["entity_category"] = entity_category

        # Name / Friendly Name
        if "name" not in attributes:
            if isinstance(self._config.get("name"), str):
                attributes["name"] = self._config["name"]
            else:
                attributes["name"] = parts[-1] if parts else (
                    topic.split("/")[-1] if topic else "entity")

        # Unique ID derived from topic, optionally with a prefix
        if "unique_id" not in attributes:
            prefix = self._config.get("unique_prefix")
            base_id = topic.replace(
                "/", "_") if isinstance(topic, str) else "entity"
            attributes["unique_id"] = f"{prefix}_{base_id}" if isinstance(
                prefix, str) and prefix else base_id

        # Merge metric info if any
        if isinstance(metric_info, dict):
            attributes.update(metric_info)

        return attributes

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Process JSON payload to extract additional attributes."""
        out: Dict[str, Any] = dict(attributes or {})
        if not isinstance(payload, str):
            return out

        try:
            parsed = json.loads(payload)
        except Exception:
            # Not JSON; nothing to add here
            return out

        if not isinstance(parsed, dict):
            return out

        # Include selected JSON attributes if configured; otherwise include scalar top-level items
        if self._json_attributes:
            for key in self._json_attributes:
                if key in parsed:
                    out[key] = parsed[key]
        else:
            for k, v in parsed.items():
                if not isinstance(v, (dict, list)):
                    out[k] = v

        # Attempt to include GPS attributes from parsed object
        gps_attrs = self.get_gps_attributes(out.get("topic", ""), parsed)
        if gps_attrs:
            out.update(gps_attrs)

        return out

    def determine_entity_category(self, category: str) -> Optional["EntityCategory"]:
        """Determine EntityCategory from attribute category."""
        if not isinstance(category, str) or not category:
            return None

        cat_norm = category.strip().lower()

        # Try to import Home Assistant's EntityCategory if available
        entity_category_enum = None
        try:
            from homeassistant.helpers.entity import EntityCategory as HAEntityCategory  # type: ignore
            entity_category_enum = HAEntityCategory
        except Exception:
            entity_category_enum = None

        # Map common string categories to EntityCategory
        diag_aliases = {"diagnostic", "diagnostics", "diag"}
        conf_aliases = {"config", "configuration",
                        "configure", "setup", "settings"}

        if entity_category_enum is None:
            # If HA not available, return None to avoid leaking non-enum types
            if cat_norm in diag_aliases or cat_norm in conf_aliases:
                return None
            return None

        if cat_norm in diag_aliases:
            return entity_category_enum.DIAGNOSTIC
        if cat_norm in conf_aliases:
            return entity_category_enum.CONFIG

        return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Extract and prepare GPS-related attributes."""
        data: Dict[str, Any] = {}

        # Normalize payload to a dict if possible
        obj: Optional[Dict[str, Any]] = None
        if isinstance(payload, dict):
            obj = payload
        elif isinstance(payload, str):
            # Try JSON first
            try:
                p = json.loads(payload)
                if isinstance(p, dict):
                    obj = p
            except Exception:
                obj = None
            # Fallback: comma or space separated "lat,lon"
            if obj is None:
                coords = self._parse_simple_coords(payload)
                if coords:
                    data["latitude"] = coords[0]
                    data["longitude"] = coords[1]
                    return data

        if obj is None:
            return data

        # Extract values
        lat = self._search_numeric(obj, self._gps_lat_keys)
        lon = self._search_numeric(obj, self._gps_lon_keys)

        # If not found at top-level, check common nesting under 'gps' or 'location'
        if lat is None or lon is None:
            for nest_key in ("gps", "location", "loc", "position", "coords", "coordinate"):
                nested = obj.get(nest_key)
                if isinstance(nested, dict):
                    if lat is None:
                        lat = self._search_numeric(nested, self._gps_lat_keys)
                    if lon is None:
                        lon = self._search_numeric(nested, self._gps_lon_keys)
                if lat is not None and lon is not None:
                    break

        # As an absolute fallback, try deep recursive search
        if lat is None:
            lat = self._deep_search_numeric(obj, self._gps_lat_keys)
        if lon is None:
            lon = self._deep_search_numeric(obj, self._gps_lon_keys)

        if lat is not None and lon is not None and self._valid_lat_lon(lat, lon):
            data["latitude"] = lat
            data["longitude"] = lon

        # Optional secondary attributes
        acc = self._search_first_numeric(
            obj, [self._gps_acc_keys, ["gps_accuracy", "accuracy_m", "accuracyMeters"]])
        if acc is not None:
            data["gps_accuracy"] = acc

        alt = self._search_first_numeric(
            obj, [self._gps_alt_keys, ["elevation"]])
        if alt is not None:
            data["altitude"] = alt

        spd = self._search_first_numeric(obj, [self._gps_spd_keys])
        if spd is not None:
            data["speed"] = spd

        brg = self._search_first_numeric(obj, [self._gps_brg_keys])
        if brg is not None:
            data["bearing"] = brg

        ts = self._search_first(obj, [self._gps_ts_keys])
        ts_val = self._normalize_timestamp(ts)
        if ts_val is not None:
            data["timestamp"] = ts_val

        return data

    # Helpers

    def _parse_simple_coords(self, s: str) -> Optional[tuple[float, float]]:
        txt = s.strip()
        if not txt:
            return None
        # Replace semicolons with commas, then split
        normalized = txt.replace(";", ",").replace("|", ",")
        parts = [p for p in normalized.replace(" ", ",").split(",") if p]
        if len(parts) < 2:
            return None
        try:
            lat = float(parts[0])
            lon = float(parts[1])
        except Exception:
            return None
        if self._valid_lat_lon(lat, lon):
            return lat, lon
        return None

    def _valid_lat_lon(self, lat: float, lon: float) -> bool:
        return -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0

    def _to_float(self, v: Any) -> Optional[float]:
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return None
            try:
                return float(s)
            except Exception:
                return None
        return None

    def _search_numeric(self, obj: Dict[str, Any], keys: List[str]) -> Optional[float]:
        for k in keys:
            if k in obj:
                val = self._to_float(obj[k])
                if val is not None:
                    return val
        return None

    def _deep_search_numeric(self, obj: Dict[str, Any], keys: List[str]) -> Optional[float]:
        # Depth-first search for numeric value under given keys
        stack: List[Any] = [obj]
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                for k, v in cur.items():
                    if isinstance(k, str) and k in keys:
                        num = self._to_float(v)
                        if num is not None:
                            return num
                    if isinstance(v, (dict, list)):
                        stack.append(v)
            elif isinstance(cur, list):
                for v in cur:
                    if isinstance(v, (dict, list)):
                        stack.append(v)
        return None

    def _search_first_numeric(self, obj: Dict[str, Any], keys_groups: List[List[str]]) -> Optional[float]:
        for group in keys_groups:
            val = self._search_numeric(obj, group)
            if val is not None:
                return val
        return None

    def _search_first(self, obj: Dict[str, Any], keys_groups: List[List[str]]) -> Any:
        for group in keys_groups:
            for k in group:
                if k in obj:
                    return obj[k]
        return None

    def _normalize_timestamp(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        # Allow numeric epoch seconds/milliseconds
        if isinstance(value, (int, float)):
            # Heuristic: if value is too large, assume milliseconds
            try:
                if value > 10_000_000_000:  # > year ~2286 in seconds; so likely ms
                    value = value / 1000.0
                dt = datetime.utcfromtimestamp(float(value))
                return dt.isoformat() + "Z"
            except Exception:
                return None
        # Try to parse ISO-like strings and return as-is if looks valid
        if isinstance(value, str):
            s = value.strip()
            if not s:
                return None
            # If already ISO-like, return as-is
            if any(ch in s for ch in ("T", "-")):
                return s
            # Maybe numeric string
            try:
                num = float(s)
                return self._normalize_timestamp(num)
            except Exception:
                return None
        return None
