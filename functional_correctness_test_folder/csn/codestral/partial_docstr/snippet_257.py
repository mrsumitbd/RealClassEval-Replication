
class UserProfileService:
    ''' Class encapsulating user profile service functionality.
  Override with your own implementation for storing and retrieving the user profile. '''

    def lookup(self, user_id: str) -> dict[str, Any]:
        user_profiles = {
            'user1': {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'},
            'user2': {'name': 'Bob', 'age': 25, 'email': 'bob@example.com'},
        }
        return user_profiles.get(user_id, {})

    def save(self, user_profile: dict[str, Any]) -> None:
        ''' Save the user profile dict sent to this method.
    Args:
      user_profile: Dict representing the user's profile.
        '''
        # In a real implementation, this would save the user profile to a database or file
        print(f"Saving user profile: {user_profile}")
