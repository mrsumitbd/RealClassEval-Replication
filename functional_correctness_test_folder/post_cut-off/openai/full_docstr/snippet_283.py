
from dataclasses import dataclass
from typing import Any, Dict, Union
import json


@dataclass
class CreateFeedModel:
    """Model for creating a feed.

    Args:
        display_name: Display name for the feed
        details: Feed details as either a JSON string or dict.
            If string, will be parsed as JSON.
    """
    display_name: str
    details: Union[str, Dict[str, Any]]

    def __post_init__(self) -> None:
        """Convert string details to dict if needed."""
        if isinstance(self.details, str):
            try:
                parsed = json.loads(self.details)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"details string is not valid JSON: {exc}") from exc
            if not isinstance(parsed, dict):
                raise ValueError("Parsed JSON must be a dictionary")
            self.details = parsed
        elif not isinstance(self.details, dict):
            raise TypeError("details must be a dict or JSON string")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "display_name": self.display_name,
            "details": self.details,
        }
