
from dataclasses import dataclass
from typing import Dict, Union


@dataclass
class Sentence:
    text: str
    length: int

    def __post_init__(self) -> None:
        self.length = len(self.text)

    def __repr__(self) -> str:
        return f"Sentence(text='{self.text}', length={self.length})"

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {'text': self.text, 'length': self.length}

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> 'Sentence':
        return cls(text=data['text'], length=data['length'])
