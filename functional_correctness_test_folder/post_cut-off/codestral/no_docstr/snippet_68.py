
import json
from typing import Dict, Any, Optional


class AgentState:

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        self.state = initial_state if initial_state is not None else {}

    def set(self, key: str, value: Any) -> None:
        self._validate_key(key)
        self._validate_json_serializable(value)
        self.state[key] = value

    def get(self, key: Optional[str] = None) -> Any:
        if key is None:
            return self.state
        self._validate_key(key)
        return self.state.get(key)

    def delete(self, key: str) -> None:
        self._validate_key(key)
        if key in self.state:
            del self.state[key]

    def _validate_key(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

    def _validate_json_serializable(self, value: Any) -> None:
        try:
            json.dumps(value)
        except (TypeError, OverflowError):
            raise ValueError("Value must be JSON serializable")
