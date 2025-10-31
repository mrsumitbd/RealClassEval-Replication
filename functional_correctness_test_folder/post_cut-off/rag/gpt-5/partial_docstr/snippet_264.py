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
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if roles is None:
            roles = []
        elif not isinstance(roles, list):
            raise TypeError("roles must be a list of strings")
        else:
            for r in roles:
                if not isinstance(r, str):
                    raise TypeError("roles must be a list of strings")

        self.id = id
        self.name = name
        self.roles = roles

    def __repr__(self) -> str:
        '''
        Return a string representation of the User.
        '''
        return f"User(id={self.id!r}, name={self.name!r}, roles={self.roles!r})"
