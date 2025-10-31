
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Any, Dict


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
    start_index: Optional[int] = field(default=None)
    end_index: Optional[int] = field(default=None)
    token_count: int = field(default=0)

    def __post_init__(self) -> None:
        """Validate context attributes."""
        if not isinstance(self.text, str):
            raise TypeError(
                f"text must be a str, got {type(self.text).__name__}")

        if self.start_index is not None and not isinstance(self.start_index, int):
            raise TypeError(
                f"start_index must be an int or None, got {type(self.start_index).__name__}"
            )
        if self.end_index is not None and not isinstance(self.end_index, int):
            raise TypeError(
                f"end_index must be an int or None, got {type(self.end_index).__name__}"
            )
        if self.start_index is not None and self.end_index is not None:
            if self.start_index > self.end_index:
                raise ValueError(
                    f"start_index ({self.start_index}) cannot be greater than end_index ({self.end_index})"
                )

        if not isinstance(self.token_count, int) or self.token_count < 0:
            raise ValueError(
                f"token_count must be a non‑negative int, got {self.token_count}"
            )

    def __len__(self) -> int:
        """Return the length of the text."""
        return len(self.text)

    def __str__(self) -> str:
        """Return a string representation of the Context."""
        return self.text

    def __repr__(self) -> str:
        """Return a detailed string representation of the Context."""
        return (
            f"{self.__class__.__name__}("
            f"text={self.text!r}, "
            f"start_index={self.start_index!r}, "
            f"end_index={self.end_index!r}, "
            f"token_count={self.token_count!r})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return the Context as a dictionary."""
        return {
            "text": self.text,
            "start_index": self.start_index,
            "end_index": self.end_index,
            "token_count": self.token_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Context":
        """Create a Context object from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError(f"data must be a dict, got {type(data).__name__}")

        # Extract values with defaults for missing keys
        text = data.get("text")
        start_index = data.get("start_index")
        end_index = data.get("end_index")
        token_count = data.get("token_count", 0)

        return cls(
            text=text,
            start_index=start_index,
            end_index=end_index,
            token_count=token_count,
        )
