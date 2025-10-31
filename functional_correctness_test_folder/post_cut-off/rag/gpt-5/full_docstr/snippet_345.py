from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EnhancedUser:
    '''增强的用户信息'''
    id: Optional[str] = None
    user_openid: Optional[str] = None
    member_openid: Optional[str] = None
    openid: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        '''从字典创建用户对象'''
        def pick(*keys: str) -> Optional[Any]:
            for k in keys:
                if k in data and data[k] is not None:
                    return data[k]
            return None

        def to_str_or_none(v: Any) -> Optional[str]:
            if v is None:
                return None
            s = str(v)
            return s if s.strip() != '' else None

        user_id = to_str_or_none(pick('id', 'ID'))
        user_openid = to_str_or_none(
            pick('user_openid', 'userOpenid', 'userOpenId', 'user_open_id'))
        member_openid = to_str_or_none(
            pick('member_openid', 'memberOpenid', 'memberOpenId', 'member_open_id'))
        openid = to_str_or_none(pick('openid', 'openId', 'open_id'))

        return cls(
            id=user_id,
            user_openid=user_openid,
            member_openid=member_openid,
            openid=openid,
            extra=dict(data) if isinstance(data, dict) else {}
        )

    def get_user_id(self) -> Optional[str]:
        '''获取用户ID，优先级：id > user_openid > member_openid > openid'''
        for v in (self.id, self.user_openid, self.member_openid, self.openid):
            if v is not None and str(v).strip() != '':
                return str(v)
        return None
