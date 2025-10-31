from dataclasses import dataclass, field
from typing import FrozenSet, Optional


@dataclass(frozen=True)
class Role:
    name: str
    manageable_roles: FrozenSet[str] = field(default_factory=frozenset)

    def can_manage_role(self, role_name: Optional[str]):
        if not isinstance(role_name, str):
            return False
        return role_name == self.name or role_name in self.manageable_roles

    def __hash__(self):
        return hash((self.name, self.manageable_roles))
