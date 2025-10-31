from dataclasses import dataclass
from typing import Dict, Optional, Union


@dataclass
class Sentence:
    text: str
    start: int = 0
    end: Optional[int] = None

    def __post_init__(self) -> None:
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        if not isinstance(self.start, int):
            raise TypeError("start must be an int")
        if self.start < 0:
            raise ValueError("start must be >= 0")

        if self.end is None:
            self.end = len(self.text)
        elif not isinstance(self.end, int):
            raise TypeError("end must be an int")
        if self.end < self.start:
            raise ValueError("end must be >= start")
        if self.end > len(self.text):
            raise ValueError("end must be <= len(text)")

    def __repr__(self) -> str:
        t = self.text
        if len(t) > 30:
            t = t[:27] + "..."
        return f"Sentence(text={t!r}, start={self.start}, end={self.end})"

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {"text": self.text, "start": self.start, "end": self.end if self.end is not None else len(self.text)}

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> 'Sentence':
        if "text" not in data:
            raise KeyError("data must contain 'text'")
        text_val = data["text"]
        if not isinstance(text_val, str):
            raise TypeError("'text' must be a string")
        start_val = data.get("start", 0)
        if not isinstance(start_val, int):
            raise TypeError("'start' must be an int")
        end_val = data.get("end", None)
        if end_val is not None and not isinstance(end_val, int):
            raise TypeError("'end' must be an int if provided")
        return cls(text=text_val, start=start_val, end=end_val)
