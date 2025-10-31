
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    name: str
    managed_roles: frozenset

    def can_manage_role(self, role_name):
        '''Determine if this role can manage the role name.'''
        return role_name in self.managed_roles

    def __hash__(self):
        return hash((self.name, self.managed_roles))
