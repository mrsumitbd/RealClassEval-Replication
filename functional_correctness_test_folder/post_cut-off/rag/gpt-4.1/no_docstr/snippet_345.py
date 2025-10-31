from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class EnhancedUser:
    '''增强的用户信息'''
    id: Optional[str] = None
    user_openid: Optional[str] = None
    member_openid: Optional[str] = None
    openid: Optional[str] = None
    # 其他可能的字段
    extra: Dict[str, Any] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        '''从字典创建用户对象'''
        id_ = data.get('id')
        user_openid = data.get('user_openid')
        member_openid = data.get('member_openid')
        openid = data.get('openid')
        # 收集除上述字段外的其他字段
        extra = {k: v for k, v in data.items() if k not in {
            'id', 'user_openid', 'member_openid', 'openid'}}
        return cls(
            id=id_,
            user_openid=user_openid,
            member_openid=member_openid,
            openid=openid,
            extra=extra if extra else {}
        )

    def get_user_id(self) -> Optional[str]:
        '''获取用户ID，优先级：id > user_openid > member_openid > openid'''
        if self.id:
            return self.id
        if self.user_openid:
            return self.user_openid
        if self.member_openid:
            return self.member_openid
        if self.openid:
            return self.openid
        return None
