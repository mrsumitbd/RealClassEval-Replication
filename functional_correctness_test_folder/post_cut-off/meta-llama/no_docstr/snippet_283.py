
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class CreateFeedModel:
    """Class for creating a feed model."""
    title: str
    content: str
    category: str

    def __post_init__(self):
        """Validate the attributes after initialization."""
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Title must be a non-empty string")
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("Content must be a non-empty string")
        if not isinstance(self.category, str) or not self.category.strip():
            raise ValueError("Category must be a non-empty string")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dictionary."""
        return asdict(self)
