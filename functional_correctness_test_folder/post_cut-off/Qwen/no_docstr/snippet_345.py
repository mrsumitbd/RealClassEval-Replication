
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class EnhancedUser:
    user_id: Optional[str] = field(default=None)
    username: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username'),
            email=data.get('email')
        )

    def get_user_id(self) -> Optional[str]:
        return self.user_id
