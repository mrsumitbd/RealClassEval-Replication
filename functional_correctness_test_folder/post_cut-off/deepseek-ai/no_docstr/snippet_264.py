
class User:

    def __init__(self, id: str, name: str, roles: list[str] = None) -> None:
        self.id = id
        self.name = name
        self.roles = roles if roles is not None else []

    def __repr__(self) -> str:
        return f"User(id='{self.id}', name='{self.name}', roles={self.roles})"
