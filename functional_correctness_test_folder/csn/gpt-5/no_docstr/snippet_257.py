from typing import Any, Dict
from copy import deepcopy
import threading


class UserProfileService:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()

    def lookup(self, user_id: str) -> dict[str, Any]:
        if not isinstance(user_id, str) or not user_id:
            raise ValueError("user_id must be a non-empty string")
        with self._lock:
            if user_id not in self._store:
                raise KeyError(f"user_id not found: {user_id}")
            return deepcopy(self._store[user_id])

    def save(self, user_profile: dict[str, Any]) -> None:
        if not isinstance(user_profile, dict):
            raise TypeError("user_profile must be a dict")
        user_id = user_profile.get("user_id") or user_profile.get("id")
        if not isinstance(user_id, str) or not user_id:
            raise ValueError(
                "user_profile must contain a non-empty 'user_id' or 'id' string")
        profile_copy = dict(user_profile)
        profile_copy["user_id"] = user_id
        with self._lock:
            self._store[user_id] = deepcopy(profile_copy)
