
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union


@dataclass
class UpdateFeedModel:
    """Model for updating a feed.

    Args:
        display_name: Optional display name for the feed
        details: Optional feed details as either a JSON string or dict.
            If string, will be parsed as JSON.
    """
    display_name: Optional[str] = None
    details: Optional[Union[str, Dict[str, Any]]] = None

    def __post_init__(self) -> None:
        """Convert string details to dict if needed."""
        if isinstance(self.details, str):
            try:
                self.details = json.loads(self.details)
            except json.JSONDecodeError as exc:
                raise ValueError("details string is not valid JSON") from exc

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: Dict[str, Any] = {}
        if self.display_name is not None:
            result["displayName"] = self.display_name
        if self.details is not None:
            result["details"] = self.details
        return result
