
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, Union


@dataclass
class CreateFeedModel:
    """Model for creating a feed entry.

    Attributes
    ----------
    id
        Unique identifier for the feed. Defaults to ``0``.
    title
        Title of the feed. Defaults to an empty string.
    details
        Additional details for the feed. Can be a JSON string or a dictionary.
        Defaults to an empty dictionary.
    """

    id: int = field(default=0)
    title: str = field(default_factory=str)
    details: Union[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Convert string details to a dictionary if needed."""
        if isinstance(self.details, str):
            try:
                self.details = json.loads(self.details)
            except json.JSONDecodeError:
                # If the string is not valid JSON, keep it as-is.
                pass

    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dictionary representation suitable for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
        }
