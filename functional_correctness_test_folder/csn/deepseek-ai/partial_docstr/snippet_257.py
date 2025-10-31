
from typing import Any, Dict


class UserProfileService:
    ''' Class encapsulating user profile service functionality.
    Override with your own implementation for storing and retrieving the user profile. '''

    def __init__(self):
        self.profiles = {}

    def lookup(self, user_id: str) -> Dict[str, Any]:
        return self.profiles.get(user_id, None)

    def save(self, user_profile: Dict[str, Any]) -> None:
        ''' Save the user profile dict sent to this method.
        Args:
            user_profile: Dict representing the user's profile.
        '''
        if 'user_id' in user_profile:
            self.profiles[user_profile['user_id']] = user_profile
