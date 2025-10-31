from dataclasses import dataclass
from typing import Any, Dict, Optional


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
        def norm(value: Any) -> Optional[str]:
            if value is None:
                return None
            s = str(value).strip()
            return s if s else None

        return cls(
            id=norm(data.get('id')),
            user_openid=norm(data.get('user_openid')),
            member_openid=norm(data.get('member_openid')),
            openid=norm(data.get('openid')),
        )

    def get_user_id(self) -> Optional[str]:
        '''获取用户ID，优先级：id > user_openid > member_openid > openid'''
        for val in (self.id, self.user_openid, self.member_openid, self.openid):
            if val is not None and str(val).strip():
                return str(val).strip()
        return None
