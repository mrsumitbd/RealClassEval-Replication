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
                self.details = {}
            else:
                parsed = json.loads(s)
                if not isinstance(parsed, dict):
                    raise ValueError('details must be a JSON object')
                self.details = parsed
        elif self.details is not None and not isinstance(self.details, dict):
            raise TypeError(
                'details must be either a dict, a JSON string, or None')

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        payload: Dict[str, Any] = {}
        if self.display_name is not None:
            payload['displayName'] = self.display_name
        if self.details is not None:
            if isinstance(self.details, dict):
                payload['details'] = self.details
            elif isinstance(self.details, str):
                parsed = json.loads(self.details)
                if not isinstance(parsed, dict):
                    raise ValueError('details must be a JSON object')
                payload['details'] = parsed
            else:
                raise TypeError(
                    'details must be either a dict, a JSON string, or None')
        return payload
