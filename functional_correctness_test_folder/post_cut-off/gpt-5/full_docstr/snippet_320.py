from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowState:
    '''Maintains the state of a multi-step workflow.'''

    current_step_id: Optional[str] = None
    step_history: List[str] = field(default_factory=list)
    responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        '''Initialize step_history with current_step_id if empty.'''
        if not self.step_history and self.current_step_id is not None:
            self.step_history.append(self.current_step_id)

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        '''Add a response for a step.'''
        if step_id not in self.responses:
            self.responses[step_id] = {}
        self.responses[step_id].update(response_values or {})
        if not self.step_history or self.step_history[-1] != step_id:
            self.step_history.append(step_id)
        self.current_step_id = step_id

    def get_all_responses(self) -> Dict[str, Any]:
        '''Get all responses flattened into a single dictionary.'''
        aggregated: Dict[str, Any] = {}
        for sid in self.step_history:
            if sid in self.responses:
                aggregated.update(self.responses[sid])
        return aggregated

    def can_go_back(self) -> bool:
        '''Check if the user can go back to a previous step.'''
        return len(self.step_history) > 1

    def go_back(self) -> Optional[str]:
        '''Go back to the previous step.'''
        if not self.can_go_back():
            return None
        self.step_history.pop()
        self.current_step_id = self.step_history[-1] if self.step_history else None
        return self.current_step_id
