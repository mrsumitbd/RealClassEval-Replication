from dataclasses import dataclass, asdict, fields, is_dataclass
from typing import Dict, Any, Type, Optional


@dataclass
class Program:

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        if data is None:
            data = {}
        cls_fields = {f.name: f for f in fields(cls)}
        kwargs: Dict[str, Any] = {}

        def _is_dataclass_type(t: Any) -> bool:
            return isinstance(t, type) and is_dataclass(t)

        for name, f in cls_fields.items():
            if name not in data:
                continue
            value = data[name]
            ftype = f.type
            if _is_dataclass_type(ftype) and isinstance(value, dict):
                if hasattr(ftype, 'from_dict') and callable(getattr(ftype, 'from_dict')):
                    value = ftype.from_dict(value)  # type: ignore
                else:
                    value = ftype(**value)  # type: ignore
            kwargs[name] = value

        return cls(**kwargs)
