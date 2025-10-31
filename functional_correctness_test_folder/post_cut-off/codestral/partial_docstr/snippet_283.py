
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class CreateFeedModel:
    details: Optional[str] = None

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            import json
            self.details = json.loads(self.details)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return {
            'details': self.details
        }
