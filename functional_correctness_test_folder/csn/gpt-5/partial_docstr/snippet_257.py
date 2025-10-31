from typing import Any, Dict
import threading
import copy


class UserProfileService:
    '''Class encapsulating user profile service functionality.
    Override with your own implementation for storing and retrieving the user profile.'''

    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()

    def lookup(self, user_id: str) -> dict[str, Any]:
        if not isinstance(user_id, str) or not user_id:
            raise ValueError("user_id must be a non-empty string")
        with self._lock:
            if user_id not in self._store:
                raise KeyError(f"User profile not found for id: {user_id}")
            return copy.deepcopy(self._store[user_id])

    def save(self, user_profile: dict[str, Any]) -> None:
        '''Save the user profile dict sent to this method.
        Args:
          user_profile: Dict representing the user's profile.
        '''
        if not isinstance(user_profile, dict):
            raise TypeError("user_profile must be a dict")
        if "id" not in user_profile:
            raise ValueError("user_profile must contain an 'id' field")
        user_id = user_profile["id"]
        if not isinstance(user_id, str) or not user_id:
            raise ValueError("'id' field must be a non-empty string")
        with self._lock:
            self._store[user_id] = copy.deepcopy(user_profile)
