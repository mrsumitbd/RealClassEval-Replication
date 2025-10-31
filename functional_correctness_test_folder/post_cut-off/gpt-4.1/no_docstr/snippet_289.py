
from dataclasses import dataclass, asdict, field
from typing import Any, Dict


@dataclass
class UpdateRuleDeployment:
    # Example fields, since none were specified
    rule_id: str = field(default="")
    version: int = field(default=1)
    active: bool = field(default=True)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.rule_id, str):
            raise TypeError("rule_id must be a string")
        if not isinstance(self.version, int):
            raise TypeError("version must be an integer")
        if not isinstance(self.active, bool):
            raise TypeError("active must be a boolean")
        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
