from typing import Any, Optional

class UserProfileService:
    """ Class encapsulating user profile service functionality.
  Override with your own implementation for storing and retrieving the user profile. """

    def lookup(self, user_id: str) -> dict[str, Any]:
        """ Fetch the user profile dict corresponding to the user ID.

    Args:
      user_id: ID for user whose profile needs to be retrieved.

    Returns:
      Dict representing the user's profile.
    """
        return UserProfile(user_id).__dict__

    def save(self, user_profile: dict[str, Any]) -> None:
        """ Save the user profile dict sent to this method.

    Args:
      user_profile: Dict representing the user's profile.
    """
        pass