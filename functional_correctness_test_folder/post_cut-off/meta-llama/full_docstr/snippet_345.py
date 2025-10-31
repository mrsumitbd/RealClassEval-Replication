
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class EnhancedUser:
    '''增强的用户信息'''
    id: Optional[str] = None
    user_openid: Optional[str] = None
    member_openid: Optional[str] = None
    openid: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        '''从字典创建用户对象'''
        return cls(**data)

    def get_user_id(self) -> Optional[str]:
        '''获取用户ID，优先级：id > user_openid > member_openid > openid'''
        for attr in ['id', 'user_openid', 'member_openid', 'openid']:
            if getattr(self, attr) is not None:
                return getattr(self, attr)
        return None
