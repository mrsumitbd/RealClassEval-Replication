
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


@dataclass
class WorkflowState:
    responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    step_history: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.responses is None:
            self.responses = {}
        if self.step_history is None:
            self.step_history = []

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        self.responses[step_id] = response_values
        if not self.step_history or self.step_history[-1] != step_id:
            self.step_history.append(step_id)

    def get_all_responses(self) -> Dict[str, Any]:
        all_responses = {}
        for resp in self.responses.values():
            all_responses.update(resp)
        return all_responses

    def can_go_back(self) -> bool:
        return len(self.step_history) > 1

    def go_back(self) -> Optional[str]:
        if self.can_go_back():
            last_step = self.step_history.pop()
            self.responses.pop(last_step, None)
            return self.step_history[-1]
        return None
