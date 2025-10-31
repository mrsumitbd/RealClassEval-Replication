from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, Iterable, Mapping, Sequence


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''

    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.__post_init__()

    def __post_init__(self):
        '''Post initilizaiton for validating/converting attributes'''
        # Sanitize all current public attributes
        keys = [k for k in self.__dict__.keys() if not k.startswith("_")]
        for k in keys:
            v = getattr(self, k)
            if v is None:
                # Drop None values from the model (treat as "not provided" on update)
                delattr(self, k)
                continue
            setattr(self, k, self._sanitize_value(v))

    def _sanitize_value(self, value: Any) -> Any:
        # Convert datetimes/dates to ISO 8601 strings
        if isinstance(value, datetime):
            # Normalize to ISO format with 'Z' if timezone-aware UTC
            if value.tzinfo is not None and value.utcoffset() is not None and value.utcoffset().total_seconds() == 0:
                return value.replace(tzinfo=None).isoformat(timespec="seconds") + "Z"
            return value.isoformat()
        if isinstance(value, date):
            return value.isoformat()

        # If value is a mapping, sanitize recursively and drop None values
        if isinstance(value, Mapping):
            sanitized: Dict[str, Any] = {}
            for k, v in value.items():
                if v is None:
                    continue
                sanitized[str(k)] = self._sanitize_value(v)
            return sanitized

        # If value is a sequence (but not string/bytes), sanitize items
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            # Flatten generators/iterables into list
            if not isinstance(value, list):
                try:
                    value = list(value)  # type: ignore[assignment]
                except TypeError:
                    pass
            return [self._sanitize_value(v) for v in value]

        # If value has a to_dict method, use it
        to_dict = getattr(value, "to_dict", None)
        if callable(to_dict):
            try:
                return to_dict()
            except Exception:
                pass

        return value

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        out: Dict[str, Any] = {}
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                continue
            if v is None:
                continue
            out[k] = self._sanitize_value(v)
        return out
