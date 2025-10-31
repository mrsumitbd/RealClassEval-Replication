from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union


class EntityCategory(str, Enum):
    CONFIG = "config"
    DIAGNOSTIC = "diagnostic"
    NONE = "none"


@dataclass(frozen=True)
class _Config:
    default_category: EntityCategory = EntityCategory.NONE
    attribute_prefix: str = ""
    json_prefix: str = "extra_"
    max_name_length: int = 128
    safe_keys: Tuple[str, ...] = (
        "latitude",
        "lat",
        "lon",
        "lng",
        "longitude",
        "alt",
        "altitude",
        "speed",
        "accuracy",
        "hacc",
        "vacc",
        "ts",
        "timestamp",
        "time",
    )


def _to_snake(parts: List[str]) -> str:
    cleaned: List[str] = []
    for p in parts:
        p = "".join(ch if ch.isalnum() or ch in (
            "-", "_") else "_" for ch in str(p))
        p = p.replace("-", "_").strip("_")
        if p:
            cleaned.append(p.lower())
    return "_".join([x for x in cleaned if x])


def _to_title(parts: List[str]) -> str:
    items: List[str] = []
    for p in parts:
        s = str(p).replace("_", " ").replace("-", " ").strip()
        if s:
            items.append(" ".join(w.capitalize() for w in s.split()))
    return " ".join(items)


def _safe_len(s: str, max_len: int) -> str:
    return s if len(s) <= max_len else s[: max_len - 1] + "…"


def _maybe_json(payload: Any) -> Optional[Union[Dict[str, Any], List[Any]]]:
    if isinstance(payload, (dict, list)):
        return payload
    if isinstance(payload, (bytes, bytearray)):
        try:
            return json.loads(payload.decode("utf-8", errors="ignore"))
        except Exception:
            return None
    if isinstance(payload, str):
        payload = payload.strip()
        if not payload:
            return None
        try:
            return json.loads(payload)
        except Exception:
            return None
    return None


def _flatten_once(d: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, dict):
            for k2, v2 in v.items():
                out[f"{k}_{k2}"] = v2
        else:
            out[k] = v
    return out


def _coerce_number(v: Any) -> Any:
    if isinstance(v, (int, float, bool)) or v is None:
        return v
    if isinstance(v, str):
        s = v.strip()
        try:
            if s.lower() in ("nan", "inf", "-inf", "+inf"):
                return None
            if "." in s or "e" in s.lower():
                return float(s)
            return int(s)
        except Exception:
            return v
    return v


def _first_present(d: Dict[str, Any], keys: List[str]) -> Optional[Any]:
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return None


class AttributeManager:
    def __init__(self, config: Dict[str, Any]):
        self._cfg = _Config(
            default_category=self._map_category(
                str(config.get("default_category", EntityCategory.NONE))
            ),
            attribute_prefix=str(config.get("attribute_prefix", "")),
            json_prefix=str(config.get("json_prefix", "extra_")),
            max_name_length=int(config.get("max_name_length", 128)),
            safe_keys=tuple(
                config.get(
                    "safe_keys",
                    (
                        "latitude",
                        "lat",
                        "lon",
                        "lng",
                        "longitude",
                        "alt",
                        "altitude",
                        "speed",
                        "accuracy",
                        "hacc",
                        "vacc",
                        "ts",
                        "timestamp",
                        "time",
                    ),
                )
            ),
        )

    def prepare_attributes(
        self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict] = None
    ) -> Dict[str, Any]:
        obj_id = _to_snake(parts or [topic])
        name = _safe_len(
            _to_title(parts or [topic]), self._cfg.max_name_length)
        ent_cat = self.determine_entity_category(
            category) or self._cfg.default_category
        out: Dict[str, Any] = {
            "topic": topic,
            "object_id": obj_id,
            "name": name,
            "category": ent_cat.value if isinstance(ent_cat, EntityCategory) else ent_cat,
        }
        if metric_info:
            if "unit" in metric_info and metric_info["unit"] is not None:
                out["unit_of_measurement"] = str(metric_info["unit"])
            if "device_class" in metric_info and metric_info["device_class"]:
                out["device_class"] = str(metric_info["device_class"])
            if "state_class" in metric_info and metric_info["state_class"]:
                out["state_class"] = str(metric_info["state_class"])
            if "icon" in metric_info and metric_info["icon"]:
                out["icon"] = str(metric_info["icon"])
            if "precision" in metric_info and metric_info["precision"] is not None:
                out["precision"] = int(metric_info["precision"])
        if self._cfg.attribute_prefix:
            prefixed = {}
            for k, v in out.items():
                prefixed[f"{self._cfg.attribute_prefix}{k}"] = v
            return prefixed
        return out

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        parsed = _maybe_json(payload)
        if not isinstance(parsed, dict):
            return dict(attributes)
        flat = _flatten_once(parsed)
        extras: Dict[str, Any] = dict(attributes)
        for k, v in flat.items():
            if not isinstance(k, str) or not k:
                continue
            if not (isinstance(v, (str, int, float, bool)) or v is None):
                continue
            key = f"{self._cfg.json_prefix}{_to_snake([k])}"
            if key in extras:
                continue
            val = _coerce_number(v)
            extras[key] = val
        return extras

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        return self._map_category(category)

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        data = _maybe_json(payload)
        if not isinstance(data, dict):
            return {}
        lat = _first_present(
            data, ["lat", "latitude", "y", "coord_lat", "gps_lat", "Latitude"]
        )
        lon = _first_present(
            data, ["lon", "lng", "longitude", "x",
                   "coord_lon", "gps_lon", "Longitude"]
        )
        alt = _first_present(
            data, ["alt", "altitude", "elevation", "Altitude"])
        hacc = _first_present(data, ["hacc", "accuracy", "hdop", "h_accuracy"])
        vacc = _first_present(data, ["vacc", "vdop", "v_accuracy"])
        spd = _first_present(data, ["speed", "spd", "velocity"])
        ts = _first_present(
            data, ["ts", "timestamp", "time", "datetime", "iso_time"])

        out: Dict[str, Any] = {}
        if lat is not None and lon is not None:
            try:
                out["latitude"] = float(lat)
                out["longitude"] = float(lon)
            except Exception:
                pass
        if alt is not None:
            try:
                out["altitude"] = float(alt)
            except Exception:
                pass
        if hacc is not None:
            try:
                out["horizontal_accuracy"] = float(hacc)
            except Exception:
                pass
        if vacc is not None:
            try:
                out["vertical_accuracy"] = float(vacc)
            except Exception:
                pass
        if spd is not None:
            try:
                out["speed"] = float(spd)
            except Exception:
                pass
        if ts is not None:
            out["timestamp"] = str(ts)

        if topic:
            out["source_topic"] = topic
        return out

    def _map_category(self, category: Optional[str]) -> EntityCategory:
        if category is None:
            return EntityCategory.NONE
        c = str(category).strip().lower()
        if c in ("diag", "diagnostic", "diagnostics", "health", "status"):
            return EntityCategory.DIAGNOSTIC
        if c in ("cfg", "config", "configuration", "setup"):
            return EntityCategory.CONFIG
        if c in ("none", "", "default", "normal", "primary"):
            return EntityCategory.NONE
        return EntityCategory.NONE
