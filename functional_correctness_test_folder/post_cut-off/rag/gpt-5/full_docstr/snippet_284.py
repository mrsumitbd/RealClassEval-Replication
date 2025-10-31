from dataclasses import dataclass
from typing import Any, Dict, Optional, Union
import json


@dataclass
class UpdateFeedModel:
    '''Model for updating a feed.
    Args:
        display_name: Optional display name for the feed
        details: Optional feed details as either a JSON string or dict.
            If string, will be parsed as JSON.
    '''
    display_name: Optional[str] = None
    details: Optional[Union[str, Dict[str, Any]]] = None

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            s = self.details.strip()
            if not s:
                self.details = None
            else:
                try:
                    parsed = json.loads(s)
                except json.JSONDecodeError as e:
                    raise ValueError(
                        "details must be a valid JSON string") from e
                if not isinstance(parsed, dict):
                    raise TypeError(
                        "details JSON must represent an object (dictionary)")
                self.details = parsed
        elif self.details is not None and not isinstance(self.details, dict):
            raise TypeError("details must be a dict, a JSON string, or None")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        data: Dict[str, Any] = {}
        if self.display_name is not None:
            data['display_name'] = self.display_name
        if self.details is not None:
            data['details'] = self.details
        return data
