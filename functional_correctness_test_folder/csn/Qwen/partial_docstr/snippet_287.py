
from dataclasses import dataclass, field
from typing import Set


@dataclass(frozen=True)
class Role:
    name: str
    manageable_roles: Set[str] = field(default_factory=set)

    def can_manage_role(self, role_name: str) -> bool:
        return role_name in self.manageable_roles

    def __hash__(self):
        return hash(self.name)
