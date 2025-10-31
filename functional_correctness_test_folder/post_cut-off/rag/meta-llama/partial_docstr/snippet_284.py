
from dataclasses import dataclass, asdict
import json
from typing import Dict, Any, Optional


@dataclass
class UpdateFeedModel:
    '''Model for updating a feed.
    Args:
        display_name: Optional display name for the feed
        details: Optional feed details as either a JSON string or dict.
            If string, will be parsed as JSON.
    '''
    display_name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            self.details = json.loads(self.details)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return asdict(self)
