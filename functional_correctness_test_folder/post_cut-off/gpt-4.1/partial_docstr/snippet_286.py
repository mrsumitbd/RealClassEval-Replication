
class NavigationAction:
    '''Represents a navigation action for a suggested action.'''

    def __init__(self, target_uri: str):
        '''Initialize a navigation action.
        Args:
            target_uri: The target URI for the navigation action
        '''
        self.target_uri = target_uri

    def __repr__(self) -> str:
        return f"NavigationAction(target_uri={self.target_uri!r})"
