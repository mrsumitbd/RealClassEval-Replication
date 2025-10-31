
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    '''Role class.'''
    name: str

    def can_manage_role(self, role_name):
        '''Determine if this role can manage the role name.'''
        hierarchy = {
            'admin': 3,
            'manager': 2,
            'user': 1,
            'guest': 0
        }
        my_level = hierarchy.get(self.name, -1)
        other_level = hierarchy.get(role_name, -1)
        return my_level > other_level

    def __hash__(self):
        '''Compute a hash for use with e.g. sets.'''
        return hash(self.name)
