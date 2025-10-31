class User:
    '''
    Represents a user and their roles.
    '''

    def __init__(self, id: str, name: str, roles: list[str] = None) -> None:
        '''
        Initializes a User instance with a unique ID, name, and roles.
        Args:
            id (str): The user's unique ID.
            name (str): The user's name.
            roles (list, optional): The user's roles. Defaults to empty list.
        '''
        self.id = id
        self.name = name
        if roles is None:
            self.roles = []
        else:
            self.roles = list(roles)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, roles={self.roles!r})"
