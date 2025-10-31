
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class WorkflowState:
    '''Maintains the state of a multi-step workflow.'''
    step_history: list[str] = field(default_factory=list)
    responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    current_step_id: Optional[str] = None

    def __post_init__(self):
        '''Initialize step_history with current_step_id if empty.'''
        if self.current_step_id and not self.step_history:
            self.step_history = [self.current_step_id]

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        '''Add a response for a step.'''
        self.responses[step_id] = response_values
        if step_id not in self.step_history:
            self.step_history.append(step_id)
        self.current_step_id = step_id

    def get_all_responses(self) -> Dict[str, Any]:
        '''Get all responses flattened into a single dictionary.'''
        all_responses = {}
        for step_responses in self.responses.values():
            all_responses.update(step_responses)
        return all_responses

    def can_go_back(self) -> bool:
        '''Check if the user can go back to a previous step.'''
        return len(self.step_history) > 1

    def go_back(self) -> Optional[str]:
        '''Go back to the previous step.'''
        if self.can_go_back():
            self.step_history.pop()
            self.current_step_id = self.step_history[-1]
            return self.current_step_id
        return None
