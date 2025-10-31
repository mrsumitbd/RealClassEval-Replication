
import json
from typing import Any, Dict, Optional


class AgentState:
    '''Represents an Agent's stateful information outside of context provided to a model.
    Provides a key-value store for agent state with JSON serialization validation and persistence support.
    Key features:
    - JSON serialization validation on assignment
    - Get/set/delete operations
    '''

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        '''Initialize AgentState.'''
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
        '''Get a value or entire state.
        Args:
            key: The key to retrieve (if None, returns entire state object)
        Returns:
            The stored value, entire state dict, or None if not found
        '''
        if key is None:
            return dict(self._state)
        return self._state.get(key, None)

    def delete(self, key: str) -> None:
        '''Delete a specific key from the state.
        Args:
            key: The key to delete
        '''
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
        if not key:
            raise ValueError("Key must not be empty")
        if key.startswith("_"):
            raise ValueError("Key must not start with underscore")

    def _validate_json_serializable(self, value: Any) -> None:
        '''Validate that a value is JSON serializable.
        Args:
            value: The value to validate
        Raises:
            ValueError: If value is not JSON serializable
        '''
        try:
            json.dumps(value)
        except (TypeError, OverflowError) as e:
            raise ValueError(f"Value is not JSON serializable: {e}")
