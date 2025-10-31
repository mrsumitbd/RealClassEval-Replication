
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class UpdateRuleDeployment:
    # Assuming some attributes for demonstration purposes
    id: int
    name: str
    description: str

    def __post_init__(self):
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("ID must be a positive integer")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
