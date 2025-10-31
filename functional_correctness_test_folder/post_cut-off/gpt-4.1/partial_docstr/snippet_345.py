
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class EnhancedUser:
    '''增强的用户信息'''
    user_id: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        user_id = data.get('user_id')
        name = data.get('name')
        email = data.get('email')
        # Collect any extra fields not explicitly defined
        extra = {k: v for k, v in data.items() if k not in {
            'user_id', 'name', 'email'}}
        return cls(user_id=user_id, name=name, email=email, extra=extra)

    def get_user_id(self) -> Optional[str]:
        return self.user_id
