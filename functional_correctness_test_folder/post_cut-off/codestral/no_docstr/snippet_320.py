
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class WorkflowState:
    responses: Dict[str, Any] = None
    current_step: str = None
    history: list = None

    def __post_init__(self):
        if self.responses is None:
            self.responses = {}
        if self.history is None:
            self.history = []

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        self.responses[step_id] = response_values
        self.current_step = step_id
        self.history.append(step_id)

    def get_all_responses(self) -> Dict[str, Any]:
        return self.responses

    def can_go_back(self) -> bool:
        return len(self.history) > 1

    def go_back(self) -> Optional[str]:
        if self.can_go_back():
            self.history.pop()
            self.current_step = self.history[-1]
            return self.current_step
        return None
