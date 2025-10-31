
from __future__ import annotations
from typing import Any, Dict


class UserProfileService:
    """Class encapsulating user profile service functionality.
    Stores and retrieves user profiles in memory.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def lookup(self, user_id: str) -> Dict[str, Any]:
        """Retrieve a user profile by user_id.

        Args:
            user_id: The unique identifier for the user.

        Returns:
            The user profile dictionary.

        Raises:
            KeyError: If the user_id is not found.
        """
        if user_id not in self._store:
            raise KeyError(f"User ID '{user_id}' not found.")
        return self._store[user_id].copy()

    def save(self, user_profile: Dict[str, Any]) -> None:
        """Save the user profile dict sent to this method.

        Args:
            user_profile: Dict representing the user's profile. Must contain a 'user_id' key.
        """
        if "user_id" not in user_profile:
            raise ValueError("user_profile must contain a 'user_id' key.")
        user_id = str(user_profile["user_id"])
        self._store[user_id] = user_profile.copy()
