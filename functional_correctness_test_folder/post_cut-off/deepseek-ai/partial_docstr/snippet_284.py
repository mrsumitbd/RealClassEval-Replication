
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class UpdateFeedModel:

    def __post_init__(self):
        '''Convert string details to dict if needed'''
        pass

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
