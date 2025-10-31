
from dataclasses import dataclass
from typing import Optional


@dataclass
class Context:
    '''Context class to hold chunk metadata.
    Attributes:
        text (str): The text of the chunk.
        start_index (Optional[int]): The starting index of the chunk in the original text.
        end_index (Optional[int]): The ending index of the chunk in the original text.
        token_count (int): The number of tokens in the chunk.
    '''
    text: str
    start_index: Optional[int] = None
    end_index: Optional[int] = None
    token_count: int = 0

    def __post_init__(self) -> None:
        '''Validate context attributes.'''
        if self.start_index is not None and self.end_index is not None:
            if self.start_index > self.end_index:
                raise ValueError(
                    "start_index cannot be greater than end_index")
        if self.token_count < 0:
            raise ValueError("token_count cannot be negative")

    def __len__(self) -> int:
        '''Return the length of the text.'''
        return len(self.text)

    def __str__(self) -> str:
        '''Return a string representation of the Context.'''
        return self.text

    def __repr__(self) -> str:
        '''Return a detailed string representation of the Context.'''
        return f"Context(text={self.text!r}, start_index={self.start_index}, end_index={self.end_index}, token_count={self.token_count})"

    def to_dict(self) -> dict:
        '''Return the Context as a dictionary.'''
        return {
            'text': self.text,
            'start_index': self.start_index,
            'end_index': self.end_index,
            'token_count': self.token_count
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Context':
        '''Create a Context object from a dictionary.'''
        return cls(
            text=data['text'],
            start_index=data.get('start_index'),
            end_index=data.get('end_index'),
            token_count=data.get('token_count', 0)
        )
