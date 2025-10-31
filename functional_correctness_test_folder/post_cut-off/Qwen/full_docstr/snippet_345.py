
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class EnhancedUser:
    '''增强的用户信息'''
    id: Optional[str] = field(default=None)
    user_openid: Optional[str] = field(default=None)
    member_openid: Optional[str] = field(default=None)
    openid: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        '''从字典创建用户对象'''
        return cls(**data)

    def get_user_id(self) -> Optional[str]:
        '''获取用户ID，优先级：id > user_openid > member_openid > openid'''
        return self.id or self.user_openid or self.member_openid or self.openid
