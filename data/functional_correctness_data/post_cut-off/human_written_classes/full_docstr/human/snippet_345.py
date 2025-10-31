from dataclasses import dataclass
from typing import Dict, Any, Optional, Union

@dataclass
class EnhancedUser:
    """增强的用户信息"""
    id: Optional[str] = None
    username: Optional[str] = None
    avatar: Optional[str] = None
    bot: Optional[bool] = None
    openid: Optional[str] = None
    user_openid: Optional[str] = None
    member_openid: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        """从字典创建用户对象"""
        return cls(id=data.get('id'), username=data.get('username'), avatar=data.get('avatar'), bot=data.get('bot'), openid=data.get('openid'), user_openid=data.get('user_openid'), member_openid=data.get('member_openid'))

    def get_user_id(self) -> Optional[str]:
        """获取用户ID，优先级：id > user_openid > member_openid > openid"""
        return self.id or self.user_openid or self.member_openid or self.openid