
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Union
import json


@dataclass
class CreateFeedModel:
    details: Union[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            try:
                self.details = json.loads(self.details)
            except Exception:
                self.details = {}

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return asdict(self)
