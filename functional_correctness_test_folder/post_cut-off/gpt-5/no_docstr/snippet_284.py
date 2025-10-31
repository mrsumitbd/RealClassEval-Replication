from dataclasses import dataclass, field, fields
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse


@dataclass
class UpdateFeedModel:
    id: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None
    last_updated: Optional[Union[datetime, str]] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        def _norm_str(v: Optional[str]) -> Optional[str]:
            if v is None:
                return None
            s = str(v).strip()
            return s if s else None

        self.id = _norm_str(self.id)
        self.title = _norm_str(self.title)
        self.url = _norm_str(self.url)
        self.description = _norm_str(self.description)

        if self.tags is not None:
            normalized: List[str] = []
            seen = set()
            for t in self.tags:
                if t is None:
                    continue
                s = str(t).strip()
                if not s or s in seen:
                    continue
                seen.add(s)
                normalized.append(s)
            self.tags = normalized if normalized else None

        if isinstance(self.last_updated, str):
            s = self.last_updated.strip()
            if s:
                try:
                    if s.endswith("Z"):
                        s = s.replace("Z", "+00:00")
                    dt = datetime.fromisoformat(s)
                except Exception:
                    dt = None
                self.last_updated = dt
            else:
                self.last_updated = None

        if isinstance(self.last_updated, datetime):
            dt = self.last_updated
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
            self.last_updated = dt

        if self.url is not None:
            parsed = urlparse(self.url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                self.url = None

        if self.extra is None:
            self.extra = {}
        else:
            cleaned_extra: Dict[str, Any] = {}
            for k, v in self.extra.items():
                if k is None:
                    continue
                key = str(k).strip()
                if not key:
                    continue
                cleaned_extra[key] = v
            self.extra = cleaned_extra

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for f in fields(self):
            name = f.name
            if name == "extra":
                continue
            value = getattr(self, name)
            if value is None:
                continue
            if isinstance(value, datetime):
                out[name] = value.astimezone(
                    timezone.utc).isoformat().replace("+00:00", "Z")
            else:
                out[name] = value

        for k, v in self.extra.items():
            if k not in out and v is not None:
                out[k] = v

        return out
