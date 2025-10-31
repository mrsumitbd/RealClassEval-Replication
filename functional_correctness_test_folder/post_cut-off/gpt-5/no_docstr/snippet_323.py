from typing import Any, Dict, List, Optional, Iterable, Tuple
from enum import Enum
import json
from datetime import datetime
import re


class EntityCategory(Enum):
    CONFIG = "config"
    DIAGNOSTIC = "diagnostic"
    SYSTEM = "system"
    NONE = "none"


class AttributeManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        self.name_template: Optional[str] = self.config.get("name_template")
        self.device_class_map: Dict[str, str] = self.config.get(
            "device_class_map", {})
        self.category_map: Dict[str, str] = self.config.get("category_map", {})
        self.default_attributes: Dict[str, Any] = self.config.get(
            "default_attributes", {})
        self.json_keys: Optional[List[str]] = self.config.get("json_keys")
        self.flatten_nested: bool = bool(
            self.config.get("flatten_nested", True))
        self.lowercase_keys: bool = bool(
            self.config.get("lowercase_keys", True))
        self._gps_key_aliases = {
            "latitude": {"lat", "latitude", "y"},
            "longitude": {"lon", "lng", "long", "longitude", "x"},
            "accuracy": {"acc", "accuracy", "hacc", "hdop"},
            "bearing": {"bear", "bearing", "course", "heading"},
            "speed": {"spd", "speed", "velocity"},
            "timestamp": {"ts", "time", "timestamp", "datetime", "t"},
        }

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        attrs: Dict[str, Any] = {}
        attrs.update(self.default_attributes)

        entity_cat = self.determine_entity_category(category)
        if entity_cat is not None:
            attrs["entity_category"] = entity_cat.value

        if category in self.device_class_map:
            attrs["device_class"] = self.device_class_map[category]

        attrs["topic"] = topic
        attrs["category"] = category

        name = None
        if isinstance(self.name_template, str):
            try:
                name = self.name_template.format(
                    topic=topic,
                    category=category,
                    parts=parts,
                    last=parts[-1] if parts else "",
                )
            except Exception:
                name = None
        if not name:
            name = parts[-1] if parts else topic
        attrs["name"] = name

        if metric_info:
            for k, v in metric_info.items():
                if v is not None:
                    attrs[k] = v

        return attrs

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        out = dict(attributes) if attributes else {}
        try:
            data = json.loads(payload)
        except Exception:
            return out

        if isinstance(data, dict):
            flat = self._flatten_dict(data) if self.flatten_nested else data
            for k, v in flat.items():
                key = str(k)
                if self.lowercase_keys:
                    key = key.lower()
                out[key] = v

            gps = self._extract_gps_from_dict(data)
            if gps:
                out.update(gps)

        elif isinstance(data, list):
            out["items"] = data

        return out

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        if not category:
            return None
        cat_str = self.category_map.get(category, category).strip().lower()

        if cat_str in {"config", "configuration"}:
            return EntityCategory.CONFIG
        if cat_str in {"diag", "diagnostic"}:
            return EntityCategory.DIAGNOSTIC
        if cat_str in {"system", "sys"}:
            return EntityCategory.SYSTEM
        if cat_str in {"none", "primary", "sensor", "default"}:
            return EntityCategory.NONE
        return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        attrs: Dict[str, Any] = {"topic": topic}

        data_obj: Optional[Dict[str, Any]] = None
        if isinstance(payload, str):
            try:
                parsed = json.loads(payload)
                if isinstance(parsed, dict):
                    data_obj = parsed
            except Exception:
                data_obj = None
        elif isinstance(payload, dict):
            data_obj = payload

        if data_obj:
            gps = self._extract_gps_from_dict(data_obj)
            if gps:
                attrs.update(gps)

        if "latitude" in attrs and "longitude" in attrs:
            attrs["source"] = topic

        return attrs

    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
        items: Dict[str, Any] = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items

    def _coerce_float(self, v: Any) -> Optional[float]:
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return None
            try:
                # Handle comma decimals
                s = s.replace(",", ".") if s.count(
                    ",") == 1 and s.count(".") == 0 else s
                return float(s)
            except Exception:
                return None
        return None

    def _match_key(self, key: str, aliases: Iterable[str]) -> bool:
        k = key.lower()
        if k in aliases:
            return True
        # common nested naming like "gps.lat"
        parts = re.split(r"[._/:-]+", k)
        return any(p in aliases for p in parts)

    def _extract_gps_from_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Search shallow and nested keys for GPS related values
        def all_items(obj: Any, prefix: str = "") -> Iterable[Tuple[str, Any]]:
            if isinstance(obj, dict):
                for kk, vv in obj.items():
                    new_key = f"{prefix}.{kk}" if prefix else str(kk)
                    yield (new_key, vv)
                    yield from all_items(vv, new_key)
            elif isinstance(obj, list):
                for idx, vv in enumerate(obj):
                    new_key = f"{prefix}[{idx}]" if prefix else f"[{idx}]"
                    yield (new_key, vv)
                    yield from all_items(vv, new_key)

        found: Dict[str, Any] = {}
        for k, v in all_items(data):
            base_key = k.split(".")[-1]
            # Latitude
            if "latitude" not in found and self._match_key(base_key, self._gps_key_aliases["latitude"]):
                lat = self._coerce_float(v)
                if lat is not None and -90.0 <= lat <= 90.0:
                    found["latitude"] = lat
                    continue
            # Longitude
            if "longitude" not in found and self._match_key(base_key, self._gps_key_aliases["longitude"]):
                lon = self._coerce_float(v)
                if lon is not None and -180.0 <= lon <= 180.0:
                    found["longitude"] = lon
                    continue
            # Accuracy
            if "gps_accuracy" not in found and self._match_key(base_key, self._gps_key_aliases["accuracy"]):
                acc = self._coerce_float(v)
                if acc is not None and acc >= 0:
                    found["gps_accuracy"] = acc
                    continue
            # Bearing
            if "bearing" not in found and self._match_key(base_key, self._gps_key_aliases["bearing"]):
                bear = self._coerce_float(v)
                if bear is not None:
                    # normalize to 0..360
                    bear = bear % 360.0
                    found["bearing"] = bear
                    continue
            # Speed
            if "speed" not in found and self._match_key(base_key, self._gps_key_aliases["speed"]):
                spd = self._coerce_float(v)
                if spd is not None:
                    found["speed"] = spd
                    continue
            # Timestamp
            if "timestamp" not in found and self._match_key(base_key, self._gps_key_aliases["timestamp"]):
                ts_val = self._parse_timestamp(v)
                if ts_val:
                    found["timestamp"] = ts_val
                    continue

        return found

    def _parse_timestamp(self, v: Any) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, (int, float)):
            # assume seconds since epoch if plausible, else ms
            val = float(v)
            if val > 1e12:  # ms
                val /= 1000.0
            try:
                return datetime.utcfromtimestamp(val).isoformat() + "Z"
            except Exception:
                return None
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return None
            # try iso
            try:
                # fromisoformat doesn't handle Z; replace if present
                iso = s.replace("Z", "+00:00") if s.endswith("Z") else s
                dt = datetime.fromisoformat(iso)
                if not dt.tzinfo:
                    return dt.isoformat() + "Z"
                return dt.astimezone(tz=None).isoformat()
            except Exception:
                pass
            # try epoch in string
            try:
                fv = float(s)
                return self._parse_timestamp(fv)
            except Exception:
                return None
        return None
