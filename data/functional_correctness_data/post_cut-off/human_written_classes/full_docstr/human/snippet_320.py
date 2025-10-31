from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class WorkflowState:
    """Maintains the state of a multi-step workflow."""
    workflow_id: str
    current_step_id: str
    step_history: List[str] = field(default_factory=list)
    responses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """Initialize step_history with current_step_id if empty."""
        if not self.step_history:
            self.step_history = [self.current_step_id]

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        """Add a response for a step."""
        self.responses[step_id] = response_values
        self.updated_at = datetime.now(timezone.utc)

    def get_all_responses(self) -> Dict[str, Any]:
        """Get all responses flattened into a single dictionary."""
        all_responses = {}
        for step_id, step_responses in self.responses.items():
            for key, value in step_responses.items():
                all_responses[f'{step_id}.{key}'] = value
                all_responses[key] = value
        return all_responses

    def can_go_back(self) -> bool:
        """Check if the user can go back to a previous step."""
        return len(self.step_history) > 1

    def go_back(self) -> Optional[str]:
        """Go back to the previous step."""
        if self.can_go_back():
            self.step_history.pop()
            previous_step = self.step_history[-1]
            self.current_step_id = previous_step
            self.updated_at = datetime.now(timezone.utc)
            return previous_step
        return None