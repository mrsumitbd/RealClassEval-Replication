
from __future__ import annotations

import json
from typing import Any, Dict, Optional


class AgentState:
    """
    A simple key/value store that validates keys and ensures values are JSON‑serializable.
    """

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        """
        Create a new AgentState instance.

        Parameters
        ----------
        initial_state : Optional[Dict[str, Any]]
            Optional dictionary to initialise the state with.
        """
        self._state: Dict[str, Any] = {}
        if initial_state is not None:
            if not isinstance(initial_state, dict):
                raise TypeError("initial_state must be a dict")
            for k, v in initial_state.items():
                self.set(k, v)

    def set(self, key: str, value: Any) -> None:
        """
        Set a key/value pair in the state.

        Parameters
        ----------
        key : str
            The key to set.
        value : Any
            The value to associate with the key. Must be JSON‑serialisable.
        """
        self._validate_key(key)
        self._validate_json_serializable(value)
        self._state[key] = value

    def get(self, key: Optional[str] = None) -> Any:
        """
        Retrieve a value from the state.

        Parameters
        ----------
        key : Optional[str]
            The key to retrieve. If None, the entire state dictionary is returned.

        Returns
        -------
        Any
            The value associated with the key, or the full state dictionary.
        """
        if key is None:
            return dict(self._state)  # return a shallow copy
        self._validate_key(key)
        if key not in self._state:
            raise KeyError(f"Key '{key}' not found in AgentState")
        return self._state[key]

    def delete(self, key: str) -> None:
        """
        Remove a key/value pair from the state.

        Parameters
        ----------
        key : str
            The key to delete.
        """
        self._validate_key(key)
        try:
            del self._state[key]
        except KeyError as exc:
            raise KeyError(f"Key '{key}' not found in AgentState") from exc

    def _validate_key(self, key: str) -> None:
        """
        Validate that a key is a non‑empty string.

        Parameters
        ----------
        key : str
            The key to validate.

        Raises
        ------
        TypeError
            If key is not a string.
        ValueError
            If key is an empty string.
        """
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string, got {type(key).__name__}")
        if key == "":
            raise ValueError("Key cannot be an empty string")

    def _validate_json_serializable(self, value: Any) -> None:
        """
        Validate that a value can be serialised to JSON.

        Parameters
        ----------
        value : Any
            The value to validate.

        Raises
        ------
        TypeError
            If the value cannot be serialised to JSON.
        """
        try:
            json.dumps(value)
        except (TypeError, OverflowError) as exc:
            raise TypeError(
                f"Value {value!r} is not JSON serialisable") from exc
