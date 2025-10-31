from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


@dataclass
class CreateFeedModel:
    title: str
    url: str
    tags: List[str] = field(default_factory=list)
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title must be a non-empty string")
        if not isinstance(self.url, str) or not self.url.strip():
            raise ValueError("url must be a non-empty string")

        self.title = self.title.strip()
        self.url = self.url.strip()

        if self.tags is None:
            self.tags = []
        if not isinstance(self.tags, list):
            raise TypeError("tags must be a list of strings")
        normalized_tags: List[str] = []
        seen = set()
        for t in self.tags:
            ts = str(t).strip()
            if ts and ts not in seen:
                seen.add(ts)
                normalized_tags.append(ts)
        self.tags = normalized_tags

        if self.metadata is None:
            self.metadata = {}
        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dict")

        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        elif not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime or None")
        elif self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=timezone.utc)

        if not isinstance(self.is_active, bool):
            raise TypeError("is_active must be a bool")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "tags": list(self.tags),
            "is_active": self.is_active,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
