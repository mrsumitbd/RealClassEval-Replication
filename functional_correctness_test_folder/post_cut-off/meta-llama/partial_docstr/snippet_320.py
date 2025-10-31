
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class WorkflowState:
    responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    current_step_id: Optional[str] = None
    step_history: list = field(default_factory=list)

    def __post_init__(self):
        if self.step_history:
            self.current_step_id = self.step_history[-1]

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        self.responses[step_id] = response_values
        if step_id not in self.step_history:
            self.step_history.append(step_id)
        self.current_step_id = step_id

    def get_all_responses(self) -> Dict[str, Any]:
        return self.responses

    def can_go_back(self) -> bool:
        return len(self.step_history) > 1

    def go_back(self) -> Optional[str]:
        if self.can_go_back():
            self.step_history.pop()
            self.current_step_id = self.step_history[-1]
            return self.current_step_id
        return None
