from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class InputInterval:
    start: Optional[float] = None
    end: Optional[float] = None
    include_start: bool = True
    include_end: bool = True
    unit: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        def pick_first(data_dict: Dict[str, Any], keys):
            for k in keys:
                if k in data_dict:
                    return data_dict[k]
            return None

        start = pick_first(
            data,
            ("start", "min", "lower", "from", "begin"),
        )
        end = pick_first(
            data,
            ("end", "max", "upper", "to", "stop"),
        )

        include_start = pick_first(
            data,
            ("include_start", "closed_start", "left_closed",
             "inclusive_start", "left_inclusive"),
        )
        include_end = pick_first(
            data,
            ("include_end", "closed_end", "right_closed",
             "inclusive_end", "right_inclusive"),
        )
        unit = data.get("unit")

        return cls(
            start=start,
            end=end,
            include_start=include_start if include_start is not None else True,
            include_end=include_end if include_end is not None else True,
            unit=unit,
        )

    def __post_init__(self):
        def coerce_number(x, name):
            if x is None:
                return None
            if isinstance(x, (int, float)):
                return float(x)
            raise TypeError(f"{name} must be a number or None")

        self.start = coerce_number(self.start, "start")
        self.end = coerce_number(self.end, "end")

        if not isinstance(self.include_start, bool):
            if self.include_start in (0, 1):
                self.include_start = bool(self.include_start)
            else:
                raise TypeError("include_start must be a bool")
        if not isinstance(self.include_end, bool):
            if self.include_end in (0, 1):
                self.include_end = bool(self.include_end)
            else:
                raise TypeError("include_end must be a bool")

        if self.unit is not None and not isinstance(self.unit, str):
            raise TypeError("unit must be a string or None")

        if self.start is not None and self.end is not None:
            if self.start > self.end:
                raise ValueError("start cannot be greater than end")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "start": self.start,
            "end": self.end,
            "include_start": self.include_start,
            "include_end": self.include_end,
            "unit": self.unit,
        }
