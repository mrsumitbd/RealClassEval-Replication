
from dataclasses import dataclass, field
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
            self.details = json.loads(self.details)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return {
            'display_name': self.display_name,
            'details': self.details
        }
