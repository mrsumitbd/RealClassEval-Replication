
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    name: str
    permissions: set[str]

    def can_manage_role(self, role_name):
        '''Determine if this role can manage the role name.'''
        return f"manage_{role_name}" in self.permissions

    def __hash__(self):
        return hash(self.name)
