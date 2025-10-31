
from typing import Any, Dict


class UserProfileService:

    def __init__(self):
        self._user_profiles = {}

    def lookup(self, user_id: str) -> Dict[str, Any]:
        return self._user_profiles.get(user_id, {})

    def save(self, user_profile: Dict[str, Any]) -> None:
        user_id = user_profile.get('user_id')
        if user_id:
            self._user_profiles[user_id] = user_profile
