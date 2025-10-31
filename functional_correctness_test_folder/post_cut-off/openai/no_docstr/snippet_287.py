
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class InputInterval:
    start: float
    end: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create an InputInterval instance from a dictionary.
        Expected keys: 'start' and 'end'.
        """
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary")
        try:
            start = float(data["start"])
            end = float(data["end"])
        except KeyError as exc:
            raise KeyError(f"Missing required key: {exc.args[0]}") from exc
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "Start and end must be convertible to float") from exc
        return cls(start=start, end=end)

    def __post_init__(self):
        """
        Validate that the interval is well‑formed.
        """
        if self.start > self.end:
            raise ValueError(
                f"Start ({self.start}) must not be greater than end ({self.end})")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the InputInterval instance back to a dictionary.
        """
        return {"start": self.start, "end": self.end}
