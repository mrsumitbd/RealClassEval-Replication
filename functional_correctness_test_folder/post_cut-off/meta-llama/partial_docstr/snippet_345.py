
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class EnhancedUser:
    '''增强的用户信息'''
    user_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        return cls(**data)

    def get_user_id(self) -> Optional[str]:
        return self.user_id
