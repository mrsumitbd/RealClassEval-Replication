
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class UpdateFeedModel:
    details: Any

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            import json
            self.details = json.loads(self.details)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'details': self.details
        }
