from dataclasses import dataclass
from typing import Iterator, Optional

@dataclass
class Context:
    """Context class to hold chunk metadata.

    Attributes:
        text (str): The text of the chunk.
        start_index (Optional[int]): The starting index of the chunk in the original text.
        end_index (Optional[int]): The ending index of the chunk in the original text.
        token_count (int): The number of tokens in the chunk.

    """
    text: str
    token_count: int
    start_index: Optional[int] = None
    end_index: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate context attributes."""
        if not isinstance(self.text, str):
            raise ValueError('Text must be a string.')
        if self.token_count is not None and self.token_count < 0:
            raise ValueError('Token count must be a non-negative integer.')
        if self.start_index is not None and self.start_index < 0:
            raise ValueError('Start index must be a non-negative integer.')
        if self.end_index is not None and self.end_index < 0:
            raise ValueError('End index must be a non-negative integer.')
        if self.start_index is not None and self.end_index is not None and (self.start_index > self.end_index):
            raise ValueError('Start index must be less than end index.')

    def __len__(self) -> int:
        """Return the length of the text."""
        return len(self.text)

    def __str__(self) -> str:
        """Return a string representation of the Context."""
        return self.text

    def __repr__(self) -> str:
        """Return a detailed string representation of the Context."""
        return f"Context(text='{self.text}', token_count={self.token_count}, start_index={self.start_index}, end_index={self.end_index})"

    def to_dict(self) -> dict:
        """Return the Context as a dictionary."""
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict) -> 'Context':
        """Create a Context object from a dictionary."""
        return cls(**data)