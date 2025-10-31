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
            raise TypeError("text must be a string")
        if not isinstance(self.start_index, int):
            raise TypeError("start_index must be an int")
        if not isinstance(self.end_index, int):
            raise TypeError("end_index must be an int")
        if not isinstance(self.token_count, int):
            raise TypeError("token_count must be an int")
        if self.start_index < 0 or self.end_index < 0 or self.token_count < 0:
            raise ValueError(
                "start_index, end_index, and token_count must be non-negative")
        if self.end_index < self.start_index:
            raise ValueError("end_index must be >= start_index")

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
            "token_count": self.token_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> 'Sentence':
        '''Create a Sentence object from a dictionary.'''
        return cls(
            text=data["text"],
            start_index=data["start_index"],
            end_index=data["end_index"],
            token_count=data["token_count"]
        )
