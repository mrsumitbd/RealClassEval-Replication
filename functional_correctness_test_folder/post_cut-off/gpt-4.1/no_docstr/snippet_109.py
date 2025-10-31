
from dataclasses import dataclass
from typing import Dict, Union


@dataclass
class Sentence:
    text: str
    length: int = 0

    def __post_init__(self) -> None:
        if not self.length:
            self.length = len(self.text)

    def __repr__(self) -> str:
        return f"Sentence(text={self.text!r}, length={self.length})"

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {"text": self.text, "length": self.length}

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> 'Sentence':
        return cls(text=data["text"], length=data.get("length", 0))
