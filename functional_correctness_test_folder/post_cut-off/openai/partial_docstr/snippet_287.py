
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Union

Number = Union[int, float]


@dataclass
class InputInterval:
    '''Input interval values to query.'''
    start: Number
    end: Number
    step: Optional[Number] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create an InputInterval instance from a dictionary.
        Expected keys: 'start', 'end', optionally 'step'.
        """
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary")

        try:
            start = data["start"]
            end = data["end"]
        except KeyError as exc:
            raise KeyError(f"Missing required key: {exc.args[0]}") from None

        step = data.get("step", None)

        return cls(start=start, end=end, step=step)

    def __post_init__(self):
        """
        Validate the interval values.
        """
        # Ensure numeric types
        if not isinstance(self.start, (int, float)):
            raise TypeError(
                f"start must be numeric, got {type(self.start).__name__}")
        if not isinstance(self.end, (int, float)):
            raise TypeError(
                f"end must be numeric, got {type(self.end).__name__}")

        # Validate order
        if self.start > self.end:
            raise ValueError(
                f"start ({self.start}) must be <= end ({self.end})")

        # Validate step if provided
        if self.step is not None:
            if not isinstance(self.step, (int, float)):
                raise TypeError(
                    f"step must be numeric, got {type(self.step).__name__}")
            if self.step <= 0:
                raise ValueError(f"step must be positive, got {self.step}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the InputInterval instance to a dictionary.
        """
        result: Dict[str, Any] = {
            "start": self.start,
            "end": self.end,
        }
        if self.step is not None:
            result["step"] = self.step
        return result
