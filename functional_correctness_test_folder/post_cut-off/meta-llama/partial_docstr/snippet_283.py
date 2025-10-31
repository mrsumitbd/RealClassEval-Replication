
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class CreateFeedModel:
    # Assuming the class has some fields, for example:
    name: str
    details: str | Dict[str, Any]

    def __post_init__(self):
        if isinstance(self.details, str):
            import json
            try:
                self.details = json.loads(self.details)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string for details")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
