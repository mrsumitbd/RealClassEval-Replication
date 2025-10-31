
from typing import Any


class UserProfileService:

    def __init__(self, storage: dict[str, dict[str, Any]]) -> None:
        self.storage = storage

    def lookup(self, user_id: str) -> dict[str, Any]:
        return self.storage.get(user_id, {})

    def save(self, user_profile: dict[str, Any]) -> None:
        user_id = user_profile.get('user_id')
        if user_id is None:
            raise ValueError("User profile must contain 'user_id'")
        self.storage[user_id] = user_profile


# Example usage:
if __name__ == "__main__":
    storage = {}
    service = UserProfileService(storage)

    user_profile = {
        'user_id': '123',
        'name': 'John Doe',
        'email': 'john@example.com'
    }

    service.save(user_profile)
    # Output: {'user_id': '123', 'name': 'John Doe', 'email': 'john@example.com'}
    print(service.lookup('123'))
    print(service.lookup('456'))  # Output: {}
