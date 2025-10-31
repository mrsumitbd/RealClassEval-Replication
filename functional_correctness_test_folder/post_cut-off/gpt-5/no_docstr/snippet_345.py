from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EnhancedUser:
    id: Optional[str] = None
    user_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedUser':
        if data is None:
            data = {}

        def to_str_or_none(v: Any) -> Optional[str]:
            if v is None:
                return None
            s = str(v).strip()
            return s if s else None

        def pick(d: Dict[str, Any], *keys: str) -> Any:
            for k in keys:
                if k in d and d[k] is not None:
                    return d[k]
            lower_map = {str(k).lower(): v for k, v in d.items()}
            for k in keys:
                lk = str(k).lower()
                if lk in lower_map and lower_map[lk] is not None:
                    return lower_map[lk]
            return None

        uid = pick(data, 'user_id', 'userId', 'uid', 'id', 'ID')
        name = pick(data, 'name', 'full_name', 'fullname',
                    'username', 'display_name')
        email = pick(data, 'email', 'mail', 'e-mail')

        reserved_keys = {
            'id', 'ID', 'user_id', 'userId', 'uid',
            'name', 'full_name', 'fullname', 'username', 'display_name',
            'email', 'mail', 'e-mail'
        }
        meta = {k: v for k, v in data.items() if k not in reserved_keys}

        primary_id = pick(data, 'id', 'ID')
        return cls(
            id=to_str_or_none(primary_id) or to_str_or_none(uid),
            user_id=to_str_or_none(uid),
            name=to_str_or_none(name),
            email=to_str_or_none(email),
            metadata=meta,
            raw=dict(data),
        )

    def get_user_id(self) -> Optional[str]:
        for v in (self.user_id, self.id):
            if v is not None:
                s = str(v).strip()
                if s:
                    return s

        keys = ('user_id', 'userId', 'uid', 'id', 'ID')
        for source in (self.metadata, self.raw):
            for k in keys:
                if k in source and source[k] is not None:
                    s = str(source[k]).strip()
                    if s:
                        return s
        return None
