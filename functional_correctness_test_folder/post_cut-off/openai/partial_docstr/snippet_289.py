
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class UpdateRuleDeployment:
    """Model for updating rule deployment."""
    rule_id: str
    deployment_status: str
    version: Optional[int] = None
    description: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.rule_id, str):
            raise TypeError("rule_id must be a string")
        if not isinstance(self.deployment_status, str):
            raise TypeError("deployment_status must be a string")
        if self.version is not None and not isinstance(self.version, int):
            raise TypeError("version must be an int or None")
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError("description must be a string or None")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data: Dict[str, Any] = {
            "rule_id": self.rule_id,
            "deployment_status": self.deployment_status,
        }
        if self.version is not None:
            data["version"] = self.version
        if self.description is not None:
            data["description"] = self.description
        return data
