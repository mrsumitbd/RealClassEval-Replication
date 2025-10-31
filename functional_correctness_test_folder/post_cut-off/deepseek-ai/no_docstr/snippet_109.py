
from dataclasses import dataclass
from typing import Dict, Union


@dataclass
class Sentence:
    text: str = ""
    index: int = 0

    def __post_init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Sentence(text='{self.text}', index={self.index})"

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "text": self.text,
            "index": self.index
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> 'Sentence':
        return cls(
            text=data.get("text", ""),
            index=data.get("index", 0)
        )
