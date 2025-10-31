
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowState:
    """Maintains the state of a multi-step workflow."""

    current_step_id: str
    step_history: List[str] = field(default_factory=list)
    responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize step_history with current_step_id if empty."""
        if not self.step_history:
            self.step_history.append(self.current_step_id)

    def add_response(self, step_id: str, response_values: Dict[str, Any]) -> None:
        """Add a response for a step."""
        self.responses[step_id] = response_values

    def get_all_responses(self) -> Dict[str, Any]:
        """Get all responses flattened into a single dictionary."""
        flattened: Dict[str, Any] = {}
        for step_resp in self.responses.values():
            flattened.update(step_resp)
        return flattened

    def can_go_back(self) -> bool:
        """Check if the user can go back to a previous step."""
        return len(self.step_history) > 1

    def go_back(self) -> Optional[str]:
        """Go back to the previous step."""
        if not self.can_go_back():
            return None
        # Remove the current step
        self.step_history.pop()
        # Set the new current step
        self.current_step_id = self.step_history[-1]
        return self.current_step_id
