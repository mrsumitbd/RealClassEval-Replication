from dataclasses import dataclass
from typing import Optional, Dict, Any


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
    start_index: Optional[int] = None
    end_index: Optional[int] = None
    token_count: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate context attributes."""
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")

        if (self.start_index is None) ^ (self.end_index is None):
            raise ValueError(
                "start_index and end_index must both be provided or both be None")

        if self.start_index is not None and self.end_index is not None:
            if not isinstance(self.start_index, int) or not isinstance(self.end_index, int):
                raise TypeError(
                    "start_index and end_index must be integers when provided")
            if self.start_index < 0 or self.end_index < 0:
                raise ValueError(
                    "start_index and end_index must be non-negative")
            if self.end_index < self.start_index:
                raise ValueError("end_index cannot be less than start_index")
            if (self.end_index - self.start_index) != len(self.text):
                raise ValueError(
                    "end_index - start_index must equal the length of text")

        if self.token_count is None:
            self.token_count = len(self.text.split()) if self.text else 0
        elif not isinstance(self.token_count, int):
            raise TypeError("token_count must be an integer")
        elif self.token_count < 0:
            raise ValueError("token_count must be non-negative")

    def __len__(self) -> int:
        """Return the length of the text."""
        return len(self.text)

    def __str__(self) -> str:
        """Return a string representation of the Context."""
        return self.text

    def __repr__(self) -> str:
        """Return a detailed string representation of the Context."""
        return (
            f"Context(text={self.text!r}, "
            f"start_index={self.start_index}, "
            f"end_index={self.end_index}, "
            f"token_count={self.token_count})"
        )

    def to_dict(self) -> dict:
        """Return the Context as a dictionary."""
        return {
            "text": self.text,
            "start_index": self.start_index,
            "end_index": self.end_index,
            "token_count": self.token_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Context':
        """Create a Context object from a dictionary."""
        if "text" not in data:
            raise ValueError("Missing required field 'text'")
        return cls(
            text=data["text"],
            start_index=data.get("start_index"),
            end_index=data.get("end_index"),
            token_count=data.get("token_count"),
        )
