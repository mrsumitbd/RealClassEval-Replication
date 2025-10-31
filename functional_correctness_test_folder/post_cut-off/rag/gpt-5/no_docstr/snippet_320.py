from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class WorkflowState:
    '''Maintains the state of a multi-step workflow.'''
    current_step_id: Optional[str] = None
    step_history: List[str] = field(default_factory=list)
    responses_by_step: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        '''Initialize step_history with current_step_id if empty.'''
        if not self.step_history and self.current_step_id:
            self.step_history.append(self.current_step_id)

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        '''Add a response for a step.'''
        if step_id not in self.responses_by_step:
            self.responses_by_step[step_id] = dict(response_values)
        else:
            self.responses_by_step[step_id].update(response_values)

        if not self.step_history or self.step_history[-1] != step_id:
            self.step_history.append(step_id)

        self.current_step_id = step_id

    def get_all_responses(self) -> Dict[str, Any]:
        '''Get all responses flattened into a single dictionary.'''
        flattened: Dict[str, Any] = {}
        for sid in self.step_history:
            values = self.responses_by_step.get(sid)
            if values:
                flattened.update(values)
        for sid, values in self.responses_by_step.items():
            if sid not in self.step_history and values:
                flattened.update(values)
        return flattened

    def can_go_back(self) -> bool:
        '''Check if the user can go back to a previous step.'''
        return len(self.step_history) > 1

    def go_back(self) -> Optional[str]:
        '''Go back to the previous step.'''
        if not self.can_go_back():
            return None
        self.step_history.pop()
        self.current_step_id = self.step_history[-1]
        return self.current_step_id
