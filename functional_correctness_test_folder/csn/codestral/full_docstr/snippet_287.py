
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    '''Role class.'''

    def can_manage_role(self, role_name):
        '''Determine if this role can manage the role name.'''
        return self.name == role_name

    def __hash__(self):
        '''Compute a hash for use with e.g. sets.'''
        return hash(self.name)
