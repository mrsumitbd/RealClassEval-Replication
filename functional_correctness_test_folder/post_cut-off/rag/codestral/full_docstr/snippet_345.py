
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
        return cls(
            id=data.get('id'),
            user_openid=data.get('user_openid'),
            member_openid=data.get('member_openid'),
            openid=data.get('openid')
        )

    def get_user_id(self) -> Optional[str]:
        '''获取用户ID，优先级：id > user_openid > member_openid > openid'''
        if self.id is not None:
            return self.id
        if self.user_openid is not None:
            return self.user_openid
        if self.member_openid is not None:
            return self.member_openid
        return self.openid
