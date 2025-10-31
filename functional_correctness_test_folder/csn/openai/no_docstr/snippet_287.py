
from dataclasses import dataclass, field
from typing import FrozenSet, Set


@dataclass(frozen=True)
class Role:
    name: str
    manages: FrozenSet[str] = field(default_factory=frozenset)

    def can_manage_role(self, role_name: str) -> bool:
        """Return True if this role can manage the role with the given name."""
        return role_name in self.manages

    def __hash__(self) -> int:
        """Hash based on the role name and the set of roles it can manage."""
        return hash((self.name, self.manages))
