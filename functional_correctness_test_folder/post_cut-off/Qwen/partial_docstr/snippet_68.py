
import json
from typing import Any, Dict, Optional


class AgentState:

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        self._state = initial_state if initial_state is not None else {}

    def set(self, key: str, value: Any) -> None:
        self._validate_key(key)
        self._validate_json_serializable(value)
        self._state[key] = value

    def get(self, key: Optional[str] = None) -> Any:
        if key is None:
            return self._state
        return self._state.get(key)

    def delete(self, key: str) -> None:
        self._validate_key(key)
        if key in self._state:
            del self._state[key]

    def _validate_key(self, key: str) -> None:
        if not isinstance(key, str) or not key:
            raise ValueError("Key must be a non-empty string")

    def _validate_json_serializable(self, value: Any) -> None:
        try:
            json.dumps(value)
        except (TypeError, OverflowError):
            raise ValueError("Value must be JSON serializable")
