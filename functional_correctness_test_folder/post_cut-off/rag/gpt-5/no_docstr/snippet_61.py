from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


@dataclass
class Program:
    """Represents a program in the database"""
    id: Optional[Union[int, str]] = None
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_active: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "tags": list(self.tags) if self.tags is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "metadata": dict(self.metadata) if self.metadata is not None else None,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        """Create from dictionary representation"""
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        def _get(*keys: str, default: Any = None) -> Any:
            for k in keys:
                if k in data:
                    return data[k]
            return default

        def _parse_dt(value: Any) -> Optional[datetime]:
            if value is None:
                return None
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                try:
                    return datetime.fromisoformat(value)
                except ValueError:
                    return None
            return None

        tags_val = _get("tags", default=[])
        if tags_val is None:
            tags_list: List[str] = []
        elif isinstance(tags_val, list):
            tags_list = [str(t) for t in tags_val]
        else:
            tags_list = [str(tags_val)]

        metadata_val = _get("metadata", default={})
        if metadata_val is None:
            metadata_dict: Dict[str, Any] = {}
        elif isinstance(metadata_val, dict):
            metadata_dict = dict(metadata_val)
        else:
            metadata_dict = {"value": metadata_val}

        return cls(
            id=_get("id", "program_id", "programId"),
            name=_get("name", "program_name", "programName"),
            version=_get("version"),
            description=_get("description"),
            tags=tags_list,
            created_at=_parse_dt(_get("created_at", "createdAt")),
            updated_at=_parse_dt(_get("updated_at", "updatedAt")),
            metadata=metadata_dict,
            is_active=_get("is_active", "isActive"),
        )
