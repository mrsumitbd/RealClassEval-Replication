
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class InputInterval:

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    def __post_init__(self):
        pass

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
