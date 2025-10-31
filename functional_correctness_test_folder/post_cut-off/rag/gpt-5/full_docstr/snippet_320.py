from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowState:
    '''Maintains the state of a multi-step workflow.'''

    current_step_id: str
    step_history: List[str] = field(default_factory=list)
    responses_by_step: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        '''Initialize step_history with current_step_id if empty.'''
        if not self.step_history:
            self.step_history.append(self.current_step_id)

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        '''Add a response for a step.'''
        if not isinstance(response_values, dict):
            raise TypeError("response_values must be a dict")

        # Update current step and history
        self.current_step_id = step_id
        if not self.step_history or self.step_history[-1] != step_id:
            self.step_history.append(step_id)

        # Merge/record responses for this step
        existing = self.responses_by_step.get(step_id, {})
        existing.update(response_values)
        self.responses_by_step[step_id] = existing

    def get_all_responses(self) -> Dict[str, Any]:
        '''Get all responses flattened into a single dictionary.'''
        flattened: Dict[str, Any] = {}
        for sid in self.step_history:
            values = self.responses_by_step.get(sid, {})
            flattened.update(values)
        return flattened

    def can_go_back(self) -> bool:
        '''Check if the user can go back to a previous step.'''
        return len(self.step_history) > 1

    def go_back(self) -> Optional[str]:
        '''Go back to the previous step.'''
        if not self.can_go_back():
            return None
        # Remove current step from history and set to previous
        self.step_history.pop()
        self.current_step_id = self.step_history[-1]
        return self.current_step_id
