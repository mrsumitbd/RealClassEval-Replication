
from dataclasses import dataclass, field
from typing import Any, Dict, Union
import json


@dataclass
class UpdateFeedModel:
    details: Union[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        if isinstance(self.details, str):
            try:
                self.details = json.loads(self.details)
            except Exception:
                self.details = {}

    def to_dict(self) -> Dict[str, Any]:
        return {'details': self.details}
