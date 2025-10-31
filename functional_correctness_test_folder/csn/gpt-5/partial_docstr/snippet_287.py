from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True, slots=True)
class Role:
    name: str
    manages: FrozenSet[str] = field(default_factory=frozenset)
    manage_all: bool = False

    def can_manage_role(self, role_name):
        '''Determine if this role can manage the role name.'''
        if self.manage_all:
            return True
        if not isinstance(role_name, str):
            return False
        return role_name in self.manages

    def __hash__(self):
        return hash((self.name, self.manage_all, self.manages))
