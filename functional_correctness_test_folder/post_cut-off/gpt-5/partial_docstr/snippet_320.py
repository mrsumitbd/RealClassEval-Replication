from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import copy


@dataclass
class WorkflowState:
    _responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    _history: List[str] = field(default_factory=list)
    _current_index: int = -1

    def __post_init__(self):
        if self._responses is None:
            self._responses = {}
        if self._history is None:
            self._history = []
        if not isinstance(self._current_index, int):
            self._current_index = -1
        if self._history:
            self._current_index = min(
                max(self._current_index, -1), len(self._history) - 1)

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        if not isinstance(step_id, str) or not step_id:
            raise ValueError("step_id must be a non-empty string.")
        if not isinstance(response_values, dict):
            raise ValueError("response_values must be a dict.")

        if self._current_index < len(self._history) - 1:
            self._history = self._history[: self._current_index + 1]

        if self._current_index == -1 or self._history[self._current_index] != step_id:
            self._history.append(step_id)
            self._current_index = len(self._history) - 1

        existing = self._responses.get(step_id, {})
        merged = {**existing, **response_values}
        self._responses[step_id] = merged

    def get_all_responses(self) -> Dict[str, Any]:
        return copy.deepcopy(self._responses)

    def can_go_back(self) -> bool:
        return self._current_index > 0

    def go_back(self) -> Optional[str]:
        if not self.can_go_back():
            return None
        self._current_index -= 1
        return self._history[self._current_index]
