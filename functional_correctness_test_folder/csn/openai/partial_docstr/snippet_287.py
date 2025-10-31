
from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True)
class Role:
    name: str
    manages: FrozenSet[str] = field(default_factory=frozenset)

    def can_manage_role(self, role_name: str) -> bool:
        """Determine if this role can manage the role name."""
        return role_name == self.name or role_name in self.manages

    def __hash__(self) -> int:
        return hash(self.name)
