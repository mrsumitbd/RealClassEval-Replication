
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowState:
    current_step: str
    steps: List[str]
    responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Ensure the current step is recorded in the history
        if not self.history:
            self.history.append(self.current_step)

    def add_response(self, step_id: str, response_values: Dict[str, Any]) -> None:
        """
        Store the response values for a given step and record the step in history.
        """
        self.responses[step_id] = response_values
        # Record the step in history if it's not already the last visited step
        if not self.history or self.history[-1] != step_id:
            self.history.append(step_id)
        # Update the current step to the newly added step
        self.current_step = step_id

    def get_all_responses(self) -> Dict[str, Any]:
        """
        Return a flattened dictionary of all responses.
        """
        flattened: Dict[str, Any] = {}
        for step_responses in self.responses.values():
            flattened.update(step_responses)
        return flattened

    def can_go_back(self) -> bool:
        """
        Check if the user can go back to a previous step.
        """
        # At least two steps in history means we can go back
        return len(self.history) > 1

    def go_back(self) -> Optional[str]:
        """
        Move back to the previous step if possible.
        Returns the step id that was moved back to, or None if not possible.
        """
        if not self.can_go_back():
            return None
        # Remove the current step
        self.history.pop()
        # The new current step is the last in history
        self.current_step = self.history[-1]
        return self.current_step
