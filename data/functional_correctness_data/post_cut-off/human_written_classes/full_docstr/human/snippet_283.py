import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, TypedDict, Optional, Union, Annotated

@dataclass
class CreateFeedModel:
    """Model for creating a feed.

    Args:
        display_name: Display name for the feed
        details: Feed details as either a JSON string or dict.
            If string, will be parsed as JSON.
    """
    display_name: Annotated[str, 'Display name for the feed']
    details: Annotated[Union[str, Dict[str, Any]], 'Feed details as JSON string or dict']

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