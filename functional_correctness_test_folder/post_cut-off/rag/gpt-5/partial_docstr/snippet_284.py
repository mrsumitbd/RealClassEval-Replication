from dataclasses import dataclass
from typing import Any, Dict, Optional, Union
from collections.abc import Mapping
import json
import copy


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
            raw = self.details.strip()
            if raw == "":
                self.details = None
            else:
                try:
                    parsed = json.loads(raw)
                except Exception as e:
                    raise ValueError(f"Invalid JSON for details: {e}") from e
                if not isinstance(parsed, dict):
                    raise ValueError("details JSON must represent an object")
                self.details = parsed
        elif self.details is None:
            pass
        elif isinstance(self.details, Mapping):
            self.details = dict(self.details)
        elif isinstance(self.details, dict):
            # already a dict
            pass
        else:
            raise TypeError(
                "details must be a dict, mapping, JSON string, or None")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        result: Dict[str, Any] = {}
        if self.display_name is not None:
            result["display_name"] = self.display_name
        if self.details is not None:
            result["details"] = copy.deepcopy(self.details)
        return result
