from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, Optional, Union


Scalar = Union[int, float]
Temporal = Union[datetime, date]
Value = Union[Scalar, Temporal]


def _parse_datetime(value: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def _coerce_value(v: Any) -> Any:
    if isinstance(v, str):
        dt = _parse_datetime(v)
        if dt is not None:
            return dt
        # try numeric
        try:
            if "." in v:
                return float(v)
            return int(v)
        except Exception:
            return v
    return v


@dataclass
class InputInterval:
    '''Input interval values to query.'''
    start: Optional[Value] = None
    end: Optional[Value] = None
    include_start: bool = True
    include_end: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        d = dict(data)

        # Normalize keys that may represent bounds
        start = d.pop("start", d.pop("min", d.pop("gte", d.pop("gt", None))))
        end = d.pop("end", d.pop("max", d.pop("lte", d.pop("lt", None))))

        # Inclusive flags
        include_start = d.pop("include_start", None)
        include_end = d.pop("include_end", None)

        # Combined "inclusive" pair like [True, False] or {"start":..., "end":...}
        inclusive = d.pop("inclusive", None)
        if inclusive is not None:
            if isinstance(inclusive, (list, tuple)) and len(inclusive) == 2:
                if include_start is None:
                    include_start = bool(inclusive[0])
                if include_end is None:
                    include_end = bool(inclusive[1])
            elif isinstance(inclusive, dict):
                if include_start is None and "start" in inclusive:
                    include_start = bool(inclusive["start"])
                if include_end is None and "end" in inclusive:
                    include_end = bool(inclusive["end"])

        # Derive inclusivity from gt/gte/lt/lte if not explicitly provided
        if include_start is None:
            if "gte" in data or "min" in data or "start" in data:
                include_start = True
            elif "gt" in data:
                include_start = False
        if include_end is None:
            if "lte" in data or "max" in data or "end" in data:
                include_end = True
            elif "lt" in data:
                include_end = False

        # Defaults if still None
        if include_start is None:
            include_start = True
        if include_end is None:
            include_end = False

        # Coerce values
        start = _coerce_value(start)
        end = _coerce_value(end)

        return cls(start=start, end=end, include_start=bool(include_start), include_end=bool(include_end))

    def __post_init__(self):
        # Coerce string inputs
        self.start = _coerce_value(self.start)
        self.end = _coerce_value(self.end)

        # If date, convert to datetime for consistent comparison
        if isinstance(self.start, date) and not isinstance(self.start, datetime):
            self.start = datetime.combine(self.start, datetime.min.time())
        if isinstance(self.end, date) and not isinstance(self.end, datetime):
            self.end = datetime.combine(self.end, datetime.min.time())

        # Type validation
        if self.start is not None and self.end is not None:
            s, e = self.start, self.end
            # Determine category
            is_num = isinstance(
                s, (int, float)) and isinstance(e, (int, float))
            is_time = isinstance(s, datetime) and isinstance(e, datetime)
            if not (is_num or is_time):
                raise TypeError(
                    "start and end must be both numeric or both datetime/date")

            # Ordering validation
            if s > e:
                raise ValueError("start must be less than or equal to end")
            if s == e and not (self.include_start and self.include_end):
                # Empty interval when both exclusive at a single point
                raise ValueError(
                    "empty interval: start == end but both bounds are not inclusive")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to a dictionary.'''
        def _ser(v: Any) -> Any:
            if isinstance(v, datetime):
                return v.isoformat()
            return v

        return {
            "start": _ser(self.start),
            "end": _ser(self.end),
            "include_start": bool(self.include_start),
            "include_end": bool(self.include_end),
        }
