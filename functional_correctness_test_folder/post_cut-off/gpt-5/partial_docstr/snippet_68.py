from typing import Optional, Dict, Any
import json
import re
import copy


class AgentState:

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        self._state: Dict[str, Any] = {}
        if initial_state is not None:
            if not isinstance(initial_state, dict):
                raise ValueError(
                    "initial_state must be a dict with string keys")
            for k, v in initial_state.items():
                self._validate_key(k)
                self._validate_json_serializable(v)
            # store a deep copy to prevent external mutation
            self._state = copy.deepcopy(initial_state)

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
        self._state[key] = copy.deepcopy(value)

    def get(self, key: Optional[str] = None) -> Any:
        if key is None:
            return copy.deepcopy(self._state)
        self._validate_key(key)
        value = self._state.get(key, None)
        return copy.deepcopy(value)

    def delete(self, key: str) -> None:
        '''Delete a specific key from the state.
        Args:
            key: The key to delete
        '''
        self._validate_key(key)
        self._state.pop(key, None)

    def _validate_key(self, key: str) -> None:
        '''Validate that a key is valid.
        Args:
            key: The key to validate
        Raises:
            ValueError: If key is invalid
        '''
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        if key == "":
            raise ValueError("Key must not be empty")
        if key.strip() != key:
            raise ValueError(
                "Key must not have leading or trailing whitespace")
        # Allow letters, digits, underscore, dash, and dot; must start with letter or underscore
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_\-\.]*$", key):
            raise ValueError("Key contains invalid characters")

    def _validate_json_serializable(self, value: Any) -> None:
        try:
            json.dumps(value)
        except (TypeError, OverflowError) as e:
            raise ValueError(f"Value is not JSON serializable: {e}") from e
