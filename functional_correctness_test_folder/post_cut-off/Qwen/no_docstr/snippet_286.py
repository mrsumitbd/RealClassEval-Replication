
class NavigationAction:

    def __init__(self, target_uri: str):
        self.target_uri = target_uri

    def __repr__(self) -> str:
        return f"NavigationAction(target_uri={self.target_uri!r})"
