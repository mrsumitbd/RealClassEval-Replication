
import json
from typing import Dict, Any, Optional


class AgentState:

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        self._state: Dict[str, Any] = initial_state.copy(
        ) if initial_state else {}

    def set(self, key: str, value: Any) -> None:
        '''Set a value in the state.
        Args:
            key: The key to store the value under
            value: The value to store (must be JSON serializable)
        Raises:
            ValueError: If key is invalid, or if value is not JSON serializable
        '''
        self._validate_key(key)
        self._validate_json_serializable(value)
        self._state[key] = value

    def get(self, key: Optional[str] = None) -> Any:
        if key is None:
            return self._state.copy()
        return self._state.get(key)

    def delete(self, key: str) -> None:
        '''Delete a specific key from the state.
        Args:
            key: The key to delete
        '''
        if key in self._state:
            del self._state[key]

    def _validate_key(self, key: str) -> None:
        '''Validate that a key is valid.
        Args:
            key: The key to validate
        Raises:
            ValueError: If key is invalid
        '''
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        if not key.strip():
            raise ValueError("Key cannot be empty or whitespace")

    def _validate_json_serializable(self, value: Any) -> None:
        try:
            json.dumps(value)
        except (TypeError, ValueError):
            raise ValueError("Value must be JSON serializable")
