from dataclasses import dataclass
from typing import ClassVar, Union


@dataclass(frozen=True)
class Role:
    '''Role class.'''
    name: str

    HIERARCHY: ClassVar[tuple[str, ...]] = (
        "owner",
        "admin",
        "manager",
        "moderator",
        "staff",
        "member",
        "user",
        "guest",
        "anonymous",
    )
    RANKS: ClassVar[dict[str, int]] = {r: i for i, r in enumerate(HIERARCHY)}

    def __post_init__(self):
        normalized = (self.name or "").strip().lower()
        object.__setattr__(self, "name", normalized)

    def can_manage_role(self, role_name: Union[str, "Role"]):
        '''Determine if this role can manage the role name.'''
        target = role_name.name if isinstance(
            role_name, Role) else str(role_name)
        target = target.strip().lower()
        if self.name not in self.RANKS or target not in self.RANKS:
            return False
        if self.name == target:
            return False
        return self.RANKS[self.name] < self.RANKS[target]

    def __hash__(self):
        '''Compute a hash for use with e.g. sets.'''
        return hash(("Role", self.name))
