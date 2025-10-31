
from dataclasses import dataclass, field
from typing import Dict, Union, List


@dataclass
class Sentence:
    words: List[str] = field(default_factory=list)
    length: int = 0

    def __post_init__(self) -> None:
        self.length = len(self.words)

    def __repr__(self) -> str:
        return f"Sentence(words={self.words}, length={self.length})"

    def to_dict(self) -> Dict[str, Union[str, int, List[str]]]:
        return {
            "words": self.words,
            "length": self.length
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int, List[str]]]) -> 'Sentence':
        return cls(words=data.get("words", []))
