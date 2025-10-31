
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


@dataclass
class WorkflowState:
    _responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    _step_history: List[str] = field(default_factory=list)

    def __post_init__(self):
        pass

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        self._responses[step_id] = response_values
        if step_id not in self._step_history:
            self._step_history.append(step_id)

    def get_all_responses(self) -> Dict[str, Any]:
        return self._responses

    def can_go_back(self) -> bool:
        return len(self._step_history) > 0

    def go_back(self) -> Optional[str]:
        if not self.can_go_back():
            return None
        last_step = self._step_history.pop()
        self._responses.pop(last_step, None)
        return last_step
