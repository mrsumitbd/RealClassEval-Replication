
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


@dataclass
class WorkflowState:
    responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    step_history: List[str] = field(default_factory=list)

    def __post_init__(self):
        pass

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        self.responses[step_id] = response_values
        if step_id not in self.step_history:
            self.step_history.append(step_id)

    def get_all_responses(self) -> Dict[str, Any]:
        return self.responses

    def can_go_back(self) -> bool:
        '''Check if the user can go back to a previous step.'''
        return len(self.step_history) > 1

    def go_back(self) -> Optional[str]:
        if not self.can_go_back():
            return None
        self.step_history.pop()
        return self.step_history[-1]
