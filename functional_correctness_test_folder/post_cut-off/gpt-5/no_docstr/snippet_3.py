from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, Iterable


def _serialize(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {k: _serialize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_serialize(v) for v in value]
    # Try common model patterns
    if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
        try:
            return {k: _serialize(v) for k, v in value.to_dict().items()}
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        try:
            data = {
                k: v
                for k, v in vars(value).items()
                if not k.startswith("_") and not callable(v)
            }
            return {k: _serialize(v) for k, v in data.items()}
        except Exception:
            pass
    try:
        return str(value)
    except Exception:
        return None


@dataclass
class StatusBioDTO:
    data: Dict[str, Any]

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        if model is None:
            return cls(data={})

        # Prefer explicit to_dict if available
        if hasattr(model, "to_dict") and callable(getattr(model, "to_dict")):
            try:
                raw = model.to_dict()
                if isinstance(raw, dict):
                    return cls(data={k: _serialize(v) for k, v in raw.items()})
            except Exception:
                pass

        # Fallback: extract public attributes
        try:
            attrs = {
                k: v
                for k, v in vars(model).items()
                if not k.startswith("_") and not callable(v)
            }
        except Exception:
            attrs = {}

        return cls(data={k: _serialize(v) for k, v in attrs.items()})

    def to_dict(self) -> dict:
        return dict(self.data)
