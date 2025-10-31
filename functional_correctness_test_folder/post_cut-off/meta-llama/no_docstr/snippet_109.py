
from dataclasses import dataclass, asdict
from typing import Dict, Union


@dataclass
class Sentence:
    text: str
    label: int

    def __post_init__(self) -> None:
        if not isinstance(self.text, str):
            raise TypeError("Text must be a string")
        if not isinstance(self.label, int):
            raise TypeError("Label must be an integer")

    def __repr__(self) -> str:
        return f"Sentence(text='{self.text}', label={self.label})"

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> 'Sentence':
        return cls(**data)
