from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EnhancedUser:
    """增强的用户信息"""
    id: Optional[str] = None
    user_openid: Optional[str] = None
    member_openid: Optional[str] = None
    openid: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        """从字典创建用户对象"""

        def _normalize(value: Any) -> Optional[str]:
            if value is None:
                return None
            s = str(value).strip()
            return s if s else None

        uid = (
            data.get('id') or
            data.get('user_id') or
            data.get('userId')
        )
        user_openid = (
            data.get('user_openid') or
            data.get('userOpenid') or
            data.get('user_open_id') or
            data.get('userOpenId')
        )
        member_openid = (
            data.get('member_openid') or
            data.get('memberOpenid') or
            data.get('member_open_id') or
            data.get('memberOpenId')
        )
        openid = (
            data.get('openid') or
            data.get('open_id') or
            data.get('openId')
        )

        return cls(
            id=_normalize(uid),
            user_openid=_normalize(user_openid),
            member_openid=_normalize(member_openid),
            openid=_normalize(openid),
            raw=dict(data) if isinstance(data, dict) else {}
        )

    def get_user_id(self) -> Optional[str]:
        """获取用户ID，优先级：id > user_openid > member_openid > openid"""

        def _first_non_empty(*values: Optional[str]) -> Optional[str]:
            for v in values:
                if v is not None and str(v).strip():
                    return str(v).strip()
            return None

        return _first_non_empty(self.id, self.user_openid, self.member_openid, self.openid)
