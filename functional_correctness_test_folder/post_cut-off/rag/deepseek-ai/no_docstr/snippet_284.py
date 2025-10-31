
from dataclasses import dataclass
from typing import Dict, Any, Union
import json


@dataclass
class UpdateFeedModel:
    '''Model for updating a feed.
    Args:
        display_name: Optional display name for the feed
        details: Optional feed details as either a JSON string or dict.
            If string, will be parsed as JSON.
    '''
    display_name: str = None
    details: Union[str, Dict[str, Any]] = None

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            try:
                self.details = json.loads(self.details)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string provided for details")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        result = {}
        if self.display_name is not None:
            result['display_name'] = self.display_name
        if self.details is not None:
            result['details'] = self.details
        return result
