
from dataclasses import dataclass, asdict, field
from typing import Any, Dict


@dataclass
class CreateFeedModel:
    # Example fields, since none were specified
    title: str = field(default="")
    content: str = field(default="")
    author_id: int = field(default=0)
    tags: list = field(default_factory=list)
    is_published: bool = field(default=False)

    def __post_init__(self):
        if not isinstance(self.title, str):
            raise TypeError("title must be a string")
        if not isinstance(self.content, str):
            raise TypeError("content must be a string")
        if not isinstance(self.author_id, int):
            raise TypeError("author_id must be an integer")
        if not isinstance(self.tags, list):
            raise TypeError("tags must be a list")
        if not isinstance(self.is_published, bool):
            raise TypeError("is_published must be a boolean")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
