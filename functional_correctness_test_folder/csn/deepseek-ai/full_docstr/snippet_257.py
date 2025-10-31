
from typing import Any, Dict


class UserProfileService:
    ''' Class encapsulating user profile service functionality.
    Override with your own implementation for storing and retrieving the user profile. '''

    def __init__(self):
        self.profiles = {}

    def lookup(self, user_id: str) -> Dict[str, Any]:
        ''' Fetch the user profile dict corresponding to the user ID.
        Args:
            user_id: ID for user whose profile needs to be retrieved.
        Returns:
            Dict representing the user's profile.
        '''
        return self.profiles.get(user_id, {})

    def save(self, user_profile: Dict[str, Any]) -> None:
        ''' Save the user profile dict sent to this method.
        Args:
            user_profile: Dict representing the user's profile.
        '''
        if 'user_id' in user_profile:
            self.profiles[user_profile['user_id']] = user_profile
