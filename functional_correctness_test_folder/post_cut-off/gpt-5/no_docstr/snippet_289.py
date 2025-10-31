from dataclasses import dataclass, field, is_dataclass
from typing import Any, Dict, Mapping, Iterable
from datetime import datetime, date
from enum import Enum
import copy


def _serialize_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(k): _serialize_value(v) for k, v in value.items()}
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return [_serialize_value(v) for v in value]
    if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
        return value.to_dict()
    if is_dataclass(value):
        # Fallback for dataclass instances without to_dict
        # type: ignore[attr-defined]
        return {k: _serialize_value(getattr(value, k)) for k in value.__dataclass_fields__}
    # Fallback to string representation
    return str(value)


@dataclass
class UpdateRuleDeployment:
    payload: Dict[str, Any] = field(default_factory=dict)
    include_none: bool = False

    def __post_init__(self):
        if not isinstance(self.payload, dict):
            raise TypeError("payload must be a dict")
        # Make a shallow copy to avoid external mutation side-effects
        self.payload = dict(self.payload)
        if not self.include_none:
            self.payload = {k: v for k,
                            v in self.payload.items() if v is not None}

    def to_dict(self) -> Dict[str, Any]:
        data = copy.deepcopy(self.payload)
        serialized = {str(k): _serialize_value(v) for k, v in data.items()}
        if not self.include_none:
            serialized = {k: v for k, v in serialized.items() if v is not None}
        return serialized
