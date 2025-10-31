from typing import Any, Dict, Optional
import json
import copy


class AgentState:
    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        self._state: Dict[str, Any] = {}
        if initial_state is not None:
            if not isinstance(initial_state, dict):
                raise TypeError("initial_state must be a dict or None")
            for k, v in initial_state.items():
                self._validate_key(k)
                self._validate_json_serializable(v)
            self._state = copy.deepcopy(initial_state)

    def set(self, key: str, value: Any) -> None:
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
        self._validate_key(key)
        if key not in self._state:
            raise KeyError(f"Key not found: {key}")
        del self._state[key]

    def _validate_key(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if not key:
            raise ValueError("Key must be a non-empty string")
        if key.strip() == "":
            raise ValueError("Key must not be only whitespace")

    def _validate_json_serializable(self, value: Any) -> None:
        try:
            json.dumps(value)
        except (TypeError, OverflowError) as e:
            raise TypeError(f"Value is not JSON serializable: {e}") from e
