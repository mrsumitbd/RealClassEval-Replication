
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowState:
    # Stores responses for each step
    responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    # Keeps the order of steps visited
    step_order: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Ensure internal structures are initialized
        if self.responses is None:
            self.responses = {}
        if self.step_order is None:
            self.step_order = []

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        """
        Record the response for a given step and update the step order.
        """
        if step_id in self.responses:
            # Merge new values into existing ones
            self.responses[step_id].update(response_values)
        else:
            self.responses[step_id] = dict(response_values)
        # Record the step in the order list if not already present
        if step_id not in self.step_order:
            self.step_order.append(step_id)

    def get_all_responses(self) -> Dict[str, Any]:
        """
        Return a flattened dictionary of all responses.
        Later steps override earlier ones for duplicate keys.
        """
        all_responses: Dict[str, Any] = {}
        for step_id in self.step_order:
            all_responses.update(self.responses.get(step_id, {}))
        return all_responses

    def can_go_back(self) -> bool:
        """
        Determine if there is a previous step to return to.
        """
        return len(self.step_order) > 1

    def go_back(self) -> Optional[str]:
        """
        Remove the most recent step and its responses.
        Return the removed step_id, or None if no step to go back to.
        """
        if not self.can_go_back():
            return None
        # Remove the last step
        last_step = self.step_order.pop()
        # Remove its responses
        self.responses.pop(last_step, None)
        return last_step
