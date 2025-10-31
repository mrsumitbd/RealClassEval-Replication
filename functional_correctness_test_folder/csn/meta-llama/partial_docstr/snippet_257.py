
from typing import Any, Dict


class UserProfileService:
    ''' Class encapsulating user profile service functionality.
    Override with your own implementation for storing and retrieving the user profile. '''

    def __init__(self):
        # Initialize an in-memory dictionary to store user profiles
        self.profiles = {}

    def lookup(self, user_id: str) -> Dict[str, Any]:
        # Return the user profile if it exists, otherwise return an empty dictionary
        return self.profiles.get(user_id, {})

    def save(self, user_profile: Dict[str, Any]) -> None:
        ''' Save the user profile dict sent to this method.
        Args:
          user_profile: Dict representing the user's profile.
        '''
        # Get the user_id from the user_profile dictionary
        user_id = user_profile.get('user_id')

        # Check if user_id exists in the user_profile
        if user_id is not None:
            # Save the user profile
            self.profiles[user_id] = user_profile
        else:
            # Raise an error if user_id is missing
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
    # Output: {'user_id': '12345', 'name': 'John Doe', 'email': 'john@example.com'}
    print(service.lookup('12345'))
