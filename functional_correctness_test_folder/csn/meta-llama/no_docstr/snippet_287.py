
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    name: str
    managed_roles: tuple[str, ...]

    def can_manage_role(self, role_name: str) -> bool:
        return role_name in self.managed_roles

    def __hash__(self) -> int:
        return hash(self.name)
