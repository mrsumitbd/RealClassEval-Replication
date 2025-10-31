from typing import Any, Optional, Dict
from threading import RLock
from copy import deepcopy


class UserProfileService:
    ''' Class encapsulating user profile service functionality.
  Override with your own implementation for storing and retrieving the user profile. '''

    def __init__(self, *, id_key: str = "user_id", initial_data: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        self._id_key = id_key
        self._store: Dict[str, Dict[str, Any]] = {}
        if initial_data:
            for k, v in initial_data.items():
                if not isinstance(v, dict):
                    raise TypeError("Initial data values must be dicts")
                self._store[k] = deepcopy(v)
        self._lock = RLock()

    def lookup(self, user_id: str) -> dict[str, Any]:
        ''' Fetch the user profile dict corresponding to the user ID.
    Args:
      user_id: ID for user whose profile needs to be retrieved.
    Returns:
      Dict representing the user's profile.
        '''
        if not isinstance(user_id, str) or not user_id:
            raise ValueError("user_id must be a non-empty string")
        with self._lock:
            if user_id not in self._store:
                raise KeyError(f"User profile not found for id: {user_id}")
            return deepcopy(self._store[user_id])

    def save(self, user_profile: dict[str, Any]) -> None:
        ''' Save the user profile dict sent to this method.
    Args:
      user_profile: Dict representing the user's profile.
        '''
        if not isinstance(user_profile, dict):
            raise TypeError("user_profile must be a dict")
        if self._id_key not in user_profile:
            raise KeyError(f"user_profile must contain key '{self._id_key}'")
        user_id = user_profile[self._id_key]
        if not isinstance(user_id, str) or not user_id:
            raise ValueError(f"'{self._id_key}' must be a non-empty string")
        with self._lock:
            self._store[user_id] = deepcopy(user_profile)
