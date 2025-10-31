from dataclasses import dataclass
from typing import Dict, Union


@dataclass
class Sentence:
    '''Class to represent a sentence.
    Attributes:
        text (str): The text of the sentence.
        start_index (int): The starting index of the sentence in the original text.
        end_index (int): The ending index of the sentence in the original text.
        token_count (int): The number of tokens in the sentence.
    '''
    text: str
    start_index: int
    end_index: int
    token_count: int

    def __post_init__(self) -> None:
        '''Validate attributes.'''
        if not isinstance(self.text, str):
            raise TypeError("text must be a str")
        if not isinstance(self.start_index, int):
            raise TypeError("start_index must be an int")
        if not isinstance(self.end_index, int):
            raise TypeError("end_index must be an int")
        if not isinstance(self.token_count, int):
            raise TypeError("token_count must be an int")
        if self.start_index < 0:
            raise ValueError("start_index must be >= 0")
        if self.end_index < self.start_index:
            raise ValueError("end_index must be >= start_index")
        if self.token_count < 0:
            raise ValueError("token_count must be >= 0")

    def __repr__(self) -> str:
        '''Return a string representation of the Sentence.'''
        return (f"Sentence(text={self.text!r}, start_index={self.start_index}, "
                f"end_index={self.end_index}, token_count={self.token_count})")

    def to_dict(self) -> Dict[str, Union[str, int]]:
        '''Return the Chunk as a dictionary.'''
        return {
            "text": self.text,
            "start_index": self.start_index,
            "end_index": self.end_index,
            "token_count": self.token_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> 'Sentence':
        '''Create a Sentence object from a dictionary.'''
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        required_keys = ["text", "start_index", "end_index", "token_count"]
        missing = [k for k in required_keys if k not in data]
        if missing:
            raise ValueError(
                f"Missing required fields for Sentence: {', '.join(missing)}")
        return cls(
            text=data["text"],  # type: ignore[arg-type]
            start_index=data["start_index"],  # type: ignore[arg-type]
            end_index=data["end_index"],  # type: ignore[arg-type]
            token_count=data["token_count"],  # type: ignore[arg-type]
        )
