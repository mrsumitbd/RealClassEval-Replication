
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
        self._state = {}
        if initial_state is not None:
            for key, value in initial_state.items():
                self.set(key, value)

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
        if not key:
            raise ValueError("Key cannot be empty")

    def _validate_json_serializable(self, value: Any) -> None:
        '''Validate that a value is JSON serializable.
        Args:
            value: The value to validate
        Raises:
            ValueError: If value is not JSON serializable
        '''
        try:
            json.dumps(value)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Value is not JSON serializable: {e}")
