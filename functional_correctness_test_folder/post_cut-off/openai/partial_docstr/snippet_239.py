
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


@dataclass
class Tag:
    id: Optional[int] = field(default=None)
    name: str = field(default_factory=str)
    description: Optional[str] = field(default=None)
    color: Optional[str] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tag to a dictionary for API requests."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tag":
        """Create a Tag instance from API response data."""
        # Only keep keys that match the dataclass fields
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered)
