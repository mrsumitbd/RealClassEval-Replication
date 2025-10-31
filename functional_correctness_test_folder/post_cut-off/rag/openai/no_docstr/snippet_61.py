
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Program:
    """Represents a program in the database"""

    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        result = asdict(self)
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Program":
        """Create from dictionary representation"""
        if data is None:
            return None  # type: ignore
        parsed: Dict[str, Any] = {}
        for key, value in data.items():
            if key in ("created_at", "updated_at") and isinstance(value, str):
                try:
                    parsed[key] = datetime.fromisoformat(value)
                except ValueError:
                    parsed[key] = value
            else:
                parsed[key] = value
        return cls(**parsed)
