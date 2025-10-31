
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    name: str
    permissions: set

    def can_manage_role(self, role_name):
        return role_name in self.permissions

    def __hash__(self):
        return hash((self.name, frozenset(self.permissions)))
