
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import json


@dataclass
class UpdateFeedModel:
    '''Model for updating a feed.
    Args:
        display_name: Optional display name for the feed
        details: Optional feed details as either a JSON string or dict.
            If string, will be parsed as JSON.
    '''
    display_name: Optional[str]
    details: Optional[str | Dict[str, Any]]

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            self.details = json.loads(self.details)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return asdict(self)
