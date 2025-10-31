
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class WorkflowState:
    responses: Dict[str, Any] = field(default_factory=dict)
    current_step: Optional[str] = None
    previous_steps: list = field(default_factory=list)

    def __post_init__(self):
        if self.current_step is None and self.responses:
            self.current_step = next(iter(self.responses))

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        self.responses[step_id] = response_values
        if self.current_step != step_id:
            self.previous_steps.append(self.current_step)
            self.current_step = step_id

    def get_all_responses(self) -> Dict[str, Any]:
        return self.responses

    def can_go_back(self) -> bool:
        return len(self.previous_steps) > 0

    def go_back(self) -> Optional[str]:
        if self.can_go_back():
            self.current_step = self.previous_steps.pop()
            return self.current_step
        return None
