from __future__ import annotations

import json
from typing import Any, Dict, List, Optional


class AttributeManager:
    '''Manager for entity attributes.'''

    def __init__(self, config: Dict[str, Any]):
        '''Initialize the attribute manager.'''
        self.config: Dict[str, Any] = config or {}
        # Common config keys (all optional):
        # - name_template: str with placeholders {topic}, {category}, {part0}, {parts}, etc.
        # - default_device_class: str
        # - default_state_class: str
        # - default_unit: str
        # - json_attribute_paths: Dict[str, str] mapping attribute name to dotted path in JSON
        # - attribute_mappings: Dict[str, str] mapping inbound key -> attribute key
        # - gps_keys: Dict[str, str] override keys for latitude/longitude/altitude/accuracy
        # - extra_attributes: Dict[str, Any] const attributes to inject
        self._entity_category_enum = None

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None) -> Dict[str, Any]:
        '''Prepare entity attributes.'''
        metric_info = metric_info or {}
        attrs: Dict[str, Any] = {}

        # Name
        name_template: Optional[str] = self.config.get("name_template")
        if name_template:
            fmt_data = {
                "topic": topic,
                "category": category,
                "parts": "/".join(parts),
            }
            # add specific part indices {part0}, {part1}, ...
            for i, p in enumerate(parts):
                fmt_data[f"part{i}"] = p
            try:
                attrs["name"] = name_template.format(**fmt_data)
            except Exception:
                attrs["name"] = "/".join(filter(None,
                                         [category] + parts)) or topic
        else:
            attrs["name"] = "/".join(filter(None, [category] + parts)) or topic

        # Unique ID
        attrs["unique_id"] = metric_info.get("unique_id") or topic

        # Device class, state class, and unit
        attrs["device_class"] = metric_info.get(
            "device_class") or self.config.get("default_device_class")
        attrs["state_class"] = metric_info.get(
            "state_class") or self.config.get("default_state_class")
        attrs["unit_of_measurement"] = metric_info.get(
            "unit_of_measurement") or self.config.get("default_unit")

        # Entity category
        ent_cat = metric_info.get("entity_category")
        if ent_cat is None:
            ent_cat = self.determine_entity_category(category)
        attrs["entity_category"] = ent_cat

        # Inject any additional constant attributes from config
        extra_attrs: Dict[str, Any] = self.config.get("extra_attributes") or {}
        if isinstance(extra_attrs, dict):
            attrs.update(
                {k: v for k, v in extra_attrs.items() if k not in attrs})

        return attrs

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        '''Process JSON payload to extract additional attributes.'''
        try:
            data = json.loads(payload)
        except Exception:
            return attributes

        if not isinstance(data, dict):
            return attributes

        # Direct merge with optional mapping
        mappings: Dict[str, str] = self.config.get("attribute_mappings") or {}
        for k, v in data.items():
            out_key = mappings.get(k, k)
            # Do not overwrite existing attributes unless allowed
            if out_key not in attributes:
                attributes[out_key] = v

        # Extract from dotted paths
        paths: Dict[str, str] = self.config.get("json_attribute_paths") or {}
        for out_key, path in paths.items():
            val = self._extract_path(data, path)
            if val is not None:
                attributes[out_key] = val

        return attributes

    def determine_entity_category(self, category: str) -> Optional['EntityCategory']:
        '''Determine EntityCategory from attribute category.'''
        if not category:
            return None

        enum_cls = self._get_entity_category_enum()

        normalized = str(category).strip().lower()
        mapping = {
            "config": "CONFIG",
            "configuration": "CONFIG",
            "diagnostic": "DIAGNOSTIC",
            "diagnostics": "DIAGNOSTIC",
            "system": "DIAGNOSTIC",
            "none": None,
            "": None,
        }
        target = mapping.get(normalized)
        if target is None:
            return None

        try:
            return getattr(enum_cls, target)
        except Exception:
            return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        '''Extract and prepare GPS-related attributes.'''
        data: Dict[str, Any]
        if isinstance(payload, str):
            try:
                parsed = json.loads(payload)
                data = parsed if isinstance(parsed, dict) else {}
            except Exception:
                data = {}
        elif isinstance(payload, dict):
            data = payload
        else:
            data = {}

        key_overrides: Dict[str, str] = self.config.get("gps_keys") or {}
        lat_keys = [key_overrides.get(
            "latitude") or "latitude", "lat", "Latitude", "Lat"]
        lon_keys = [key_overrides.get(
            "longitude") or "longitude", "lon", "lng", "Longitude", "Long", "Lng"]
        alt_keys = [key_overrides.get(
            "altitude") or "altitude", "alt", "Altitude", "Alt"]
        acc_keys = [key_overrides.get(
            "accuracy") or "accuracy", "acc", "hdop", "Accuracy", "Acc", "HDOP"]

        def first_present(keys: List[str]) -> Optional[Any]:
            for k in keys:
                if k in data and data[k] is not None:
                    return data[k]
            return None

        lat = first_present(lat_keys)
        lon = first_present(lon_keys)
        alt = first_present(alt_keys)
        acc = first_present(acc_keys)

        attrs: Dict[str, Any] = {}
        if lat is not None and lon is not None:
            attrs["latitude"] = self._as_float(lat)
            attrs["longitude"] = self._as_float(lon)
        if alt is not None:
            attrs["altitude"] = self._as_float(alt)
        if acc is not None:
            attrs["accuracy"] = self._as_float(acc)

        # Optional metadata
        source = self.config.get("gps_source")
        if source:
            attrs["source"] = source
        attrs.setdefault("topic", topic)

        return attrs

    def _extract_path(self, data: Dict[str, Any], path: str) -> Any:
        if not path:
            return None
        cur: Any = data
        for part in path.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                return None
        return cur

    def _get_entity_category_enum(self):
        if self._entity_category_enum is not None:
            return self._entity_category_enum

        try:
            from homeassistant.helpers.entity import EntityCategory  # type: ignore
            self._entity_category_enum = EntityCategory
            return self._entity_category_enum
        except Exception:
            pass

        # Fallback: create a lightweight enum-like object with attributes
        class _FallbackEntityCategory:
            CONFIG = "config"
            DIAGNOSTIC = "diagnostic"

        self._entity_category_enum = _FallbackEntityCategory
        return self._entity_category_enum

    def _as_float(self, value: Any) -> Optional[float]:
        try:
            return float(value)
        except Exception:
            return None
