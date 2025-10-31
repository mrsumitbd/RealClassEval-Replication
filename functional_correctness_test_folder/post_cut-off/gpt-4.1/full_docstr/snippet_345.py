
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EnhancedUser:
    '''增强的用户信息'''
    id: Optional[str] = field(default=None)
    user_openid: Optional[str] = field(default=None)
    member_openid: Optional[str] = field(default=None)
    openid: Optional[str] = field(default=None)
    # 允许存储其他字段
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        '''从字典创建用户对象'''
        known_fields = {'id', 'user_openid', 'member_openid', 'openid'}
        init_kwargs = {k: data.get(k) for k in known_fields}
        extra = {k: v for k, v in data.items() if k not in known_fields}
        return cls(**init_kwargs, extra=extra)

    def get_user_id(self) -> Optional[str]:
        '''获取用户ID，优先级：id > user_openid > member_openid > openid'''
        for attr in ['id', 'user_openid', 'member_openid', 'openid']:
            value = getattr(self, attr, None)
            if value:
                return value
        return None
