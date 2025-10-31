
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Iterable


@dataclass(frozen=True)
class Role:
    """Role class."""

    name: str
    """The name of the role."""

    manages: FrozenSet[str] = field(default_factory=frozenset)
    """A set of role names that this role can manage."""

    def can_manage_role(self, role_name: str) -> bool:
        """
        Determine if this role can manage the role name.

        A role can manage another role if the other role's name is in
        the ``manages`` set or if it is the same role.
        """
        return role_name == self.name or role_name in self.manages

    def __hash__(self) -> int:
        """
        Compute a hash for use with e.g. sets.

        The hash is based on the role's name and the frozenset of
        managed role names to ensure immutability and consistency.
        """
        return hash((self.name, self.manages))
