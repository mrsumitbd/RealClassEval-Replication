
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class CreateFeedModel:

    def __post_init__(self):
        pass

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
