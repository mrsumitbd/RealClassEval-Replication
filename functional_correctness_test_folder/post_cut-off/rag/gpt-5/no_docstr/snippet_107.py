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
        if not isinstance(self.text, str):
            raise TypeError('text must be a string')

        if self.start_index is not None and not isinstance(self.start_index, int):
            raise TypeError('start_index must be an int or None')

        if self.end_index is not None and not isinstance(self.end_index, int):
            raise TypeError('end_index must be an int or None')

        if not isinstance(self.token_count, int):
            raise TypeError('token_count must be an int')

        if self.token_count < 0:
            raise ValueError('token_count cannot be negative')

        if (self.start_index is None) != (self.end_index is None):
            raise ValueError(
                'start_index and end_index must both be set or both be None')

        if self.start_index is not None and self.end_index is not None:
            if self.start_index < 0:
                raise ValueError('start_index cannot be negative')
            if self.end_index < 0:
                raise ValueError('end_index cannot be negative')
            if self.start_index > self.end_index:
                raise ValueError(
                    'start_index cannot be greater than end_index')
            if self.end_index > len(self.text):
                raise ValueError(
                    'end_index cannot be greater than length of text')

    def __len__(self) -> int:
        '''Return the length of the text.'''
        return len(self.text)

    def __str__(self) -> str:
        '''Return a string representation of the Context.'''
        return self.text

    def __repr__(self) -> str:
        '''Return a detailed string representation of the Context.'''
        return (
            f"Context(text={self.text!r}, "
            f"start_index={self.start_index!r}, "
            f"end_index={self.end_index!r}, "
            f"token_count={self.token_count!r})"
        )

    def to_dict(self) -> dict:
        '''Return the Context as a dictionary.'''
        return {
            'text': self.text,
            'start_index': self.start_index,
            'end_index': self.end_index,
            'token_count': self.token_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Context':
        '''Create a Context object from a dictionary.'''
        if not isinstance(data, dict):
            raise TypeError('data must be a dictionary')

        return cls(
            text=data.get('text', ''),
            start_index=data.get('start_index'),
            end_index=data.get('end_index'),
            token_count=data.get('token_count', 0),
        )
