
from typing import Optional, Dict, Any
import json


class AgentState:

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        if initial_state is not None:
            if not isinstance(initial_state, dict):
                raise ValueError("initial_state must be a dictionary or None")
            # Validate all keys and values
            for k, v in initial_state.items():
                self._validate_key(k)
                self._validate_json_serializable(v)
            self._state = dict(initial_state)
        else:
            self._state = {}

    def set(self, key: str, value: Any) -> None:
        self._validate_key(key)
        self._validate_json_serializable(value)
        self._state[key] = value

    def get(self, key: Optional[str] = None) -> Any:
        if key is None:
            return dict(self._state)
        self._validate_key(key)
        return self._state.get(key, None)

    def delete(self, key: str) -> None:
        self._validate_key(key)
        if key in self._state:
            del self._state[key]

    def _validate_key(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if not key:
            raise ValueError("Key must not be empty")

    def _validate_json_serializable(self, value: Any) -> None:
        try:
            json.dumps(value)
        except (TypeError, OverflowError):
            raise ValueError("Value must be JSON serializable")
