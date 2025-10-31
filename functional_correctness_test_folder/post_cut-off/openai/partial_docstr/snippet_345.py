
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EnhancedUser:
    """增强的用户信息"""

    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnhancedUser":
        """Create an EnhancedUser instance from a dictionary."""
        return cls(data=data)

    def get_user_id(self) -> Optional[str]:
        """Return the user id if present in the data."""
        return self.data.get("user_id") or self.data.get("id")
