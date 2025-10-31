
from typing import Any, Dict


class UserProfileService:
    ''' Class encapsulating user profile service functionality.
    Override with your own implementation for storing and retrieving the user profile. '''

    def __init__(self):
        # Initialize an in-memory dictionary to store user profiles
        self.profiles = {}

    def lookup(self, user_id: str) -> Dict[str, Any]:
        ''' Fetch the user profile dict corresponding to the user ID.
        Args:
          user_id: ID for user whose profile needs to be retrieved.
        Returns:
          Dict representing the user's profile.
        '''
        return self.profiles.get(user_id)

    def save(self, user_profile: Dict[str, Any]) -> None:
        ''' Save the user profile dict sent to this method.
        Args:
          user_profile: Dict representing the user's profile.
        '''
        user_id = user_profile.get('user_id')
        if user_id is not None:
            self.profiles[user_id] = user_profile
        else:
            raise ValueError("User profile must contain 'user_id' key")


# Example usage:
if __name__ == "__main__":
    service = UserProfileService()
    user_profile = {
        'user_id': '12345',
        'name': 'John Doe',
        'email': 'john@example.com'
    }
    service.save(user_profile)
    retrieved_profile = service.lookup('12345')
    print(retrieved_profile)
