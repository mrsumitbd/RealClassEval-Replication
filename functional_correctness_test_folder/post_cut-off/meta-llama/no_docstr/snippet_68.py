
import json
from typing import Optional, Dict, Any


class AgentState:

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        self.state = initial_state if initial_state is not None else {}
        for key in self.state:
            self._validate_key(key)
            self._validate_json_serializable(self.state[key])

    def set(self, key: str, value: Any) -> None:
        self._validate_key(key)
        self._validate_json_serializable(value)
        self.state[key] = value

    def get(self, key: Optional[str] = None) -> Any:
        if key is None:
            return self.state.copy()
        self._validate_key(key)
        return self.state.get(key)

    def delete(self, key: str) -> None:
        self._validate_key(key)
        if key in self.state:
            del self.state[key]

    def _validate_key(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if not key:
            raise ValueError("Key cannot be empty")

    def _validate_json_serializable(self, value: Any) -> None:
        try:
            json.dumps(value)
        except TypeError:
            raise TypeError("Value is not JSON serializable")
