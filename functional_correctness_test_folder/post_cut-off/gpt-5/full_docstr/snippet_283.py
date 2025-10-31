from dataclasses import dataclass
from typing import Any, Dict, Union
import json


@dataclass
class CreateFeedModel:
    '''Model for creating a feed.
    Args:
        display_name: Display name for the feed
        details: Feed details as either a JSON string or dict.
            If string, will be parsed as JSON.
    '''
    display_name: str
    details: Union[str, Dict[str, Any]]

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            try:
                parsed = json.loads(self.details)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"details must be a valid JSON string: {e}") from e
            if not isinstance(parsed, dict):
                raise ValueError("details JSON must decode to a dictionary")
            self.details = parsed
        elif not isinstance(self.details, dict):
            raise TypeError("details must be either a dict or a JSON string")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return {
            "display_name": self.display_name,
            "details": self.details,
        }
