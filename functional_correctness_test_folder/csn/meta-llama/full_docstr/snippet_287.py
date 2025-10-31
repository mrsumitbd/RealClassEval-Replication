
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    '''Role class.'''
    name: str
    manageable_roles: tuple[str, ...]

    def can_manage_role(self, role_name: str) -> bool:
        '''Determine if this role can manage the role name.'''
        return role_name in self.manageable_roles

    def __hash__(self) -> int:
        '''Compute a hash for use with e.g. sets.'''
        return hash(self.name)
