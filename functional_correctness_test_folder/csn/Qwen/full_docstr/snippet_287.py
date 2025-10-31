
from dataclasses import dataclass, field
from typing import Set


@dataclass(frozen=True)
class Role:
    '''Role class.'''
    name: str
    manageable_roles: Set[str] = field(default_factory=set)

    def can_manage_role(self, role_name):
        '''Determine if this role can manage the role name.'''
        return role_name in self.manageable_roles

    def __hash__(self):
        '''Compute a hash for use with e.g. sets.'''
        return hash(self.name)
