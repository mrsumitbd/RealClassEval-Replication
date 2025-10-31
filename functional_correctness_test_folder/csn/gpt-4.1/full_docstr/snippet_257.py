
from typing import Any


class UserProfileService:
    ''' Class encapsulating user profile service functionality.
    Override with your own implementation for storing and retrieving the user profile. '''

    def __init__(self):
        self._profiles: dict[str, dict[str, Any]] = {}

    def lookup(self, user_id: str) -> dict[str, Any]:
        ''' Fetch the user profile dict corresponding to the user ID.
        Args:
          user_id: ID for user whose profile needs to be retrieved.
        Returns:
          Dict representing the user's profile.
        '''
        return self._profiles.get(user_id, {})

    def save(self, user_profile: dict[str, Any]) -> None:
        ''' Save the user profile dict sent to this method.
        Args:
          user_profile: Dict representing the user's profile.
        '''
        user_id = user_profile.get("user_id")
        if user_id is not None:
            self._profiles[user_id] = user_profile.copy()
