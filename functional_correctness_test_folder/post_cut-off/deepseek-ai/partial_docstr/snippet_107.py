
from dataclasses import dataclass
from typing import Optional, Dict, Any


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
        if self.token_count < 0:
            raise ValueError("token_count must be non-negative")
        if self.start_index is not None and self.end_index is not None:
            if self.start_index > self.end_index:
                raise ValueError("start_index must be <= end_index")

    def __len__(self) -> int:
        '''Return the length of the text.'''
        return len(self.text)

    def __str__(self) -> str:
        '''Return a string representation of the Context.'''
        return f"Context(text={self.text[:20]}..., start_index={self.start_index}, end_index={self.end_index}, token_count={self.token_count})"

    def __repr__(self) -> str:
        return f"Context(text={self.text!r}, start_index={self.start_index!r}, end_index={self.end_index!r}, token_count={self.token_count!r})"

    def to_dict(self) -> Dict[str, Any]:
        '''Return the Context as a dictionary.'''
        return {
            "text": self.text,
            "start_index": self.start_index,
            "end_index": self.end_index,
            "token_count": self.token_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Context':
        '''Create a Context from a dictionary.'''
        return cls(
            text=data.get("text", ""),
            start_index=data.get("start_index"),
            end_index=data.get("end_index"),
            token_count=data.get("token_count", 0)
        )
