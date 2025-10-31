
from __future__ import annotations

import json
from typing import Any, Dict, Optional


class AgentState:
    """
    A simple key/value store that ensures keys are valid strings and values are JSON‑serialisable.
    """

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        """
        Initialise the state with an optional dictionary.

        Args:
            initial_state: Optional dictionary of initial key/value pairs.
        """
        self._state: Dict[str, Any] = {}
        if initial_state:
            for k, v in initial_state.items():
                self.set(k, v)

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the state.

        Args:
            key: The key to store the value under.
            value: The value to store (must be JSON serialisable).

        Raises:
            ValueError: If key is invalid, or if value is not JSON serialisable.
        """
        self._validate_key(key)
        self._validate_json_serializable(value)
        self._state[key] = value

    def get(self, key: Optional[str] = None) -> Any:
        """
        Retrieve a value from the state.

        Args:
            key: The key to retrieve. If None, the entire state dictionary is returned.

        Returns:
            The value associated with the key, or the full state dictionary if key is None.
            If the key does not exist, None is returned.
        """
        if key is None:
            return dict(self._state)  # return a shallow copy
        return self._state.get(key)

    def delete(self, key: str) -> None:
        """
        Delete a specific key from the state.

        Args:
            key: The key to delete.

        Raises:
            KeyError: If the key does not exist.
        """
        if key not in self._state:
            raise KeyError(f"Key '{key}' not found in state.")
        del self._state[key]

    def _validate_key(self, key: str) -> None:
        """
        Validate that a key is valid.

        Args:
            key: The key to validate.

        Raises:
            ValueError: If key is invalid.
        """
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")
        if not key:
            raise ValueError("Key cannot be an empty string.")
        # Disallow keys that contain whitespace or control characters
        if any(c.isspace() for c in key):
            raise ValueError("Key cannot contain whitespace characters.")
        # Disallow keys that contain control characters
        if any(ord(c) < 32 or ord(c) == 127 for c in key):
            raise ValueError("Key contains invalid control characters.")

    def _validate_json_serializable(self, value: Any) -> None:
        """
        Validate that a value is JSON serialisable.

        Args:
            value: The value to validate.

        Raises:
            ValueError: If the value is not JSON serialisable.
        """
        try:
            json.dumps(value)
        except (TypeError, OverflowError) as exc:
            raise ValueError(
                f"Value {value!r} is not JSON serialisable.") from exc
