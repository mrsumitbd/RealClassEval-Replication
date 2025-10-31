
from __future__ import annotations
from typing import Any, Dict


class UserProfileService:
    """Class encapsulating user profile service functionality.

    This implementation uses an in‑memory dictionary to store user profiles.
    Each profile must contain a ``user_id`` key that uniquely identifies the
    user.  The service provides ``lookup`` and ``save`` operations.
    """

    # In‑memory store: mapping from user_id to profile dict
    _store: Dict[str, Dict[str, Any]] = {}

    def lookup(self, user_id: str) -> Dict[str, Any]:
        """Fetch the user profile dict corresponding to the user ID.

        Args:
            user_id: ID for user whose profile needs to be retrieved.

        Returns:
            Dict representing the user's profile.

        Raises:
            KeyError: If no profile exists for the given user_id.
        """
        if user_id not in self._store:
            raise KeyError(f"No profile found for user_id: {user_id}")
        # Return a shallow copy to prevent accidental mutation of the stored dict
        return dict(self._store[user_id])

    def save(self, user_profile: Dict[str, Any]) -> None:
        """Save the user profile dict sent to this method.

        Args:
            user_profile: Dict representing the user's profile. Must contain
                a ``user_id`` key.

        Raises:
            ValueError: If ``user_profile`` does not contain a ``user_id`` key.
        """
        if "user_id" not in user_profile:
            raise ValueError("user_profile must contain a 'user_id' key")
        user_id = user_profile["user_id"]
        # Store a copy to avoid external mutation affecting the internal store
        self._store[user_id] = dict(user_profile)
