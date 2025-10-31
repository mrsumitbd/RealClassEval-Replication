
from typing import Any


class UserProfileService:
    def __init__(self):
        self._profiles: dict[str, dict[str, Any]] = {}

    def lookup(self, user_id: str) -> dict[str, Any]:
        return self._profiles.get(user_id, {})

    def save(self, user_profile: dict[str, Any]) -> None:
        user_id = user_profile.get("user_id")
        if user_id is not None:
            self._profiles[user_id] = user_profile.copy()
