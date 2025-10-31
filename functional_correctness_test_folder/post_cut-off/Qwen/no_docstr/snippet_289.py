
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class UpdateRuleDeployment:

    def __post_init__(self):
        pass

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
