
import json
from typing import Any, Dict, Optional


class AgentState:

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        if initial_state is not None:
            if not isinstance(initial_state, dict):
                raise ValueError("initial_state must be a dict or None")
            # Validate all keys and values
            for k, v in initial_state.items():
                self._validate_key(k)
                self._validate_json_serializable(v)
            self._state = dict(initial_state)
        else:
            self._state = {}

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
            return dict(self._state)
        self._validate_key(key)
        return self._state.get(key, None)

    def delete(self, key: str) -> None:
        '''Delete a specific key from the state.
        Args:
            key: The key to delete
        '''
        self._validate_key(key)
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
        if not key or key.strip() == "":
            raise ValueError("Key must be a non-empty string")
        if any(c in key for c in ' \t\n\r\x0b\x0c'):
            raise ValueError("Key must not contain whitespace characters")

    def _validate_json_serializable(self, value: Any) -> None:
        try:
            json.dumps(value)
        except (TypeError, OverflowError):
            raise ValueError("Value must be JSON serializable")
