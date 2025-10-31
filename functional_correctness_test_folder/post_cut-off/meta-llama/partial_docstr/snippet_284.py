
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class UpdateFeedModel:
    # Assuming there are some fields in the dataclass
    id: int
    details: str or Dict[str, Any]

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            import json
            try:
                self.details = json.loads(self.details)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string for details")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
