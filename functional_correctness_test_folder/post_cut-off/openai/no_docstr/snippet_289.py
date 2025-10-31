
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class UpdateRuleDeployment:
    rule_id: str
    deployment_id: str
    status: str = "pending"
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.rule_id:
            raise ValueError("rule_id must not be empty")
        if not self.deployment_id:
            raise ValueError("deployment_id must not be empty")
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "deployment_id": self.deployment_id,
            "status": self.status,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
