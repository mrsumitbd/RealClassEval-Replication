class NavigationAction:

    def __init__(self, target_uri: str):
        if not isinstance(target_uri, str):
            raise TypeError("target_uri must be a string")
        target_uri = target_uri.strip()
        if not target_uri:
            raise ValueError("target_uri must be a non-empty string")
        self.target_uri = target_uri

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(target_uri={self.target_uri!r})"
