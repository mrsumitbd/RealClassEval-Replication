from dataclasses import dataclass
from typing import Any, Dict, Optional, Union
from collections.abc import Mapping
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
    details: Union[Dict[str, Any], str, None] = None

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if self.details is None:
            self.details = {}
        elif isinstance(self.details, str):
            s = self.details.strip()
            if not s:
                self.details = {}
            else:
                try:
                    parsed = json.loads(s)
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f'Invalid JSON for details: {e.msg}') from e
                if not isinstance(parsed, dict):
                    raise ValueError('details JSON must represent an object')
                self.details = parsed
        elif isinstance(self.details, Mapping):
            self.details = dict(self.details)
        elif not isinstance(self.details, dict):
            raise TypeError(
                'details must be a dict, mapping, JSON string, or None')

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return {
            'display_name': self.display_name,
            'details': self.details if self.details is not None else {},
        }
