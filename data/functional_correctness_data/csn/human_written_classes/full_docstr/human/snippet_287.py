from dataclasses import dataclass, field

@dataclass(frozen=True)
class Role:
    """Role class."""
    name: str = ''
    'Name of the role.'
    title: str = ''
    'Title of the role.'
    description: str = ''
    'Brief description of capabilities of the role.'
    can_manage_roles: list = field(default_factory=list)
    'List of other roles that this role can manage.'
    is_owner: bool = False
    'This role is the owner role (only one can exists).'
    can_manage: bool = False
    'This role has manage permissions.'
    can_curate: bool = False
    'This role has record manage permissions.'
    can_view: bool = False
    'This role has view restricted record permissions.'

    def can_manage_role(self, role_name):
        """Determine if this role can manage the role name."""
        return role_name in self.can_manage_roles

    def __hash__(self):
        """Compute a hash for use with e.g. sets."""
        return self.name.__hash__()