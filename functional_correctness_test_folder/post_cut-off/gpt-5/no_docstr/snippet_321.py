from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Dict
import json


@dataclass
class RegistryConfig:

    def to_dict(self) -> Dict[str, Any]:
        def _convert(value):
            if is_dataclass(value):
                return {f.name: _convert(getattr(value, f.name)) for f in fields(value) if getattr(value, f.name) is not None}
            if isinstance(value, dict):
                return {k: _convert(v) for k, v in value.items() if v is not None}
            if isinstance(value, (list, tuple, set)):
                return type(value)(_convert(v) for v in value if v is not None)
            return value
        result = _convert(self)
        if isinstance(result, dict):
            return result
        return {}

    def __repr__(self) -> str:
        parts = []
        for f in fields(self):
            val = getattr(self, f.name)
            if val is not None:
                parts.append(f"{f.name}={val!r}")
        return f"{self.__class__.__name__}({', '.join(parts)})"

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True, default=str)
