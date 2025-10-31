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
        if data is None:
            data = {}

        def pick(keys: list[str]) -> Optional[str]:
            for k in keys:
                if k in data and data[k] is not None:
                    v = data[k]
                    s = v if isinstance(v, str) else str(v)
                    s = s.strip()
                    if s != '':
                        return s
            return None

        return cls(
            id=pick(['id', 'user_id', 'uid', 'userId', 'UserId', 'ID', 'Id']),
            user_openid=pick(['user_openid', 'userOpenid',
                             'userOpenId', 'user_open_id', 'userOpenID']),
            member_openid=pick(['member_openid', 'memberOpenid',
                               'memberOpenId', 'member_open_id', 'memberOpenID']),
            openid=pick(['openid', 'openId', 'open_id', 'OpenId', 'OpenID']),
        )

    def get_user_id(self) -> Optional[str]:
        '''获取用户ID，优先级：id > user_openid > member_openid > openid'''
        return self.id or self.user_openid or self.member_openid or self.openid
