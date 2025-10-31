class User:

    def __init__(self, id: str, name: str, roles: list[str] = None) -> None:
        self.id = str(id)
        self.name = str(name)
        if roles is None:
            self.roles = []
        else:
            if not isinstance(roles, (list, tuple)):
                raise TypeError("roles must be a list or tuple of strings")
            self.roles = [str(r) for r in roles]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, roles={self.roles!r})"
