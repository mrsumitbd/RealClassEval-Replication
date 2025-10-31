from typing import Dict, Any, List, TypedDict, Optional, Union, Annotated
from dataclasses import dataclass, asdict
import json

@dataclass
class UpdateFeedModel:
    """Model for updating a feed.

    Args:
        display_name: Optional display name for the feed
        details: Optional feed details as either a JSON string or dict.
            If string, will be parsed as JSON.
    """
    display_name: Annotated[Optional[str], 'Optional display name for the feed'] = None
    details: Annotated[Optional[Union[str, Dict[str, Any]]], 'Optional feed details as JSON string or dict'] = None

    def __post_init__(self):
        """Convert string details to dict if needed"""
        if isinstance(self.details, str):
            try:
                self.details = json.loads(self.details)
            except json.JSONDecodeError as e:
                raise ValueError(f'Invalid JSON string for details: {e}') from e

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)