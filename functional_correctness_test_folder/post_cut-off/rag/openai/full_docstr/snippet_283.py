
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, Union


@dataclass
class CreateFeedModel:
    """Model for creating a feed.

    Args:
        display_name: Display name for the feed
        details: Feed details as either a JSON string or dict.
            If string, will be parsed as JSON.
    """

    display_name: str
    details: Union[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Convert string details to dict if needed."""
        if isinstance(self.details, str):
            try:
                self.details = json.loads(self.details)
            except json.JSONDecodeError as exc:
                raise ValueError("`details` string is not valid JSON") from exc
        if not isinstance(self.details, dict):
            raise TypeError("`details` must be a dict or a JSON string")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "displayName": self.display_name,
            "details": self.details,
        }
