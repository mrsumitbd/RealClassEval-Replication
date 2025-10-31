
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class WorkflowState:
    responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    current_step_id: Optional[str] = None
    step_order: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.step_order:
            self.current_step_id = self.step_order[0]

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        self.responses[step_id] = response_values
        if step_id in self.step_order:
            current_index = self.step_order.index(step_id)
            if current_index < len(self.step_order) - 1:
                self.current_step_id = self.step_order[current_index + 1]

    def get_all_responses(self) -> Dict[str, Any]:
        return self.responses

    def can_go_back(self) -> bool:
        if not self.current_step_id or self.current_step_id == self.step_order[0]:
            return False
        return True

    def go_back(self) -> Optional[str]:
        if not self.can_go_back():
            return None
        current_index = self.step_order.index(self.current_step_id)
        self.current_step_id = self.step_order[current_index - 1]
        return self.current_step_id
