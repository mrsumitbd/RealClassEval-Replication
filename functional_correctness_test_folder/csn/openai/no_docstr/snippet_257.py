
from typing import Any, Dict


class UserProfileService:
    _store: Dict[str, Dict[str, Any]] = {}

    def lookup(self, user_id: str) -> Dict[str, Any]:
        if user_id in self._store:
            return self._store[user_id]
        raise KeyError(f"User profile for id '{user_id}' not found")

    def save(self, user_profile: Dict[str, Any]) -> None:
        if not isinstance(user_profile, dict):
            raise TypeError("user_profile must be a dict")
        user_id = user_profile.get("user_id")
        if not user_id:
            raise ValueError("user_profile must contain 'user_id'")
        self._store[user_id] = user_profile
