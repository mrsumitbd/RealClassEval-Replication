
from dataclasses import dataclass, asdict
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
    token_count: int
    start_index: Optional[int] = None
    end_index: Optional[int] = None

    def __post_init__(self) -> None:
        '''Validate context attributes.'''
        if not isinstance(self.text, str):
            raise TypeError('text must be a string')
        if not isinstance(self.token_count, int) or self.token_count < 0:
            raise TypeError('token_count must be a non-negative integer')
        if self.start_index is not None and not isinstance(self.start_index, int):
            raise TypeError('start_index must be an integer or None')
        if self.end_index is not None and not isinstance(self.end_index, int):
            raise TypeError('end_index must be an integer or None')
        if self.start_index is not None and self.end_index is not None and self.start_index > self.end_index:
            raise ValueError('start_index cannot be greater than end_index')

    def __len__(self) -> int:
        '''Return the length of the text.'''
        return len(self.text)

    def __str__(self) -> str:
        '''Return a string representation of the Context.'''
        return self.text

    def __repr__(self) -> str:
        '''Return a detailed string representation of the Context.'''
        return f'Context(text={self.text}, start_index={self.start_index}, end_index={self.end_index}, token_count={self.token_count})'

    def to_dict(self) -> dict:
        '''Return the Context as a dictionary.'''
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Context':
        '''Create a Context object from a dictionary.'''
        return cls(**data)
