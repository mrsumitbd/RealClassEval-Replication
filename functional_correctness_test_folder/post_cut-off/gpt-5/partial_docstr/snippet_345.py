from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EnhancedUser:
    '''增强的用户信息'''
    raw: Dict[str, Any] = field(default_factory=dict)
    user_id: Optional[str] = None
    id: Optional[str] = None
    uid: Optional[str] = None
    open_id: Optional[str] = None
    union_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        data = data or {}

        # Flatten potential nested 'user' object if present
        nested_user = data.get('user')
        flat = dict(data)
        if isinstance(nested_user, dict):
            flat = {**nested_user, **{k: v for k,
                                      v in data.items() if k != 'user'}}

        # Normalize common key variants
        user_id = flat.get('user_id')
        _id = flat.get('id')
        uid = flat.get('uid')
        open_id = flat.get('open_id', flat.get('openid'))
        union_id = flat.get('union_id', flat.get('unionid'))

        known_keys = {
            'user_id', 'id', 'uid', 'open_id', 'openid', 'union_id', 'unionid', 'user'
        }
        extra = {k: v for k, v in data.items() if k not in known_keys}

        return cls(
            raw=data,
            user_id=str(user_id) if user_id is not None else None,
            id=str(_id) if _id is not None else None,
            uid=str(uid) if uid is not None else None,
            open_id=str(open_id) if open_id is not None else None,
            union_id=str(union_id) if union_id is not None else None,
            extra=extra
        )

    def get_user_id(self) -> Optional[str]:
        for val in (self.user_id, self.id, self.uid, self.open_id, self.union_id):
            if val is not None and str(val).strip() != '':
                return str(val)
        # fallback: try from raw if not mapped yet
        for key in ('user_id', 'id', 'uid', 'open_id', 'openid', 'union_id', 'unionid'):
            if key in self.raw and self.raw[key] is not None and str(self.raw[key]).strip() != '':
                return str(self.raw[key])
        # nested user fallback
        nested = self.raw.get('user')
        if isinstance(nested, dict):
            for key in ('user_id', 'id', 'uid', 'open_id', 'openid', 'union_id', 'unionid'):
                if key in nested and nested[key] is not None and str(nested[key]).strip() != '':
                    return str(nested[key])
        return None
