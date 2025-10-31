from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowState:
    responses_by_step: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.responses_by_step is None:
            self.responses_by_step = {}
        if self.history is None:
            self.history = []
        # Ensure history aligns with responses if one was prepopulated without the other
        if not self.history and self.responses_by_step:
            self.history = list(self.responses_by_step.keys())
        else:
            # Remove any steps in history that have no response stored
            self.history = [
                s for s in self.history if s in self.responses_by_step]

    def add_response(self, step_id: str, response_values: Dict[str, Any]):
        if not isinstance(step_id, str) or not step_id:
            raise ValueError("step_id must be a non-empty string")
        if response_values is None:
            response_values = {}
        if not isinstance(response_values, dict):
            raise ValueError("response_values must be a dict")

        # If step exists in history, truncate anything after it (reset future path)
        if step_id in self.history:
            idx = self.history.index(step_id)
            # Remove responses for truncated steps
            for removed_step in self.history[idx + 1:]:
                self.responses_by_step.pop(removed_step, None)
            self.history = self.history[: idx + 1]
        else:
            self.history.append(step_id)

        self.responses_by_step[step_id] = dict(response_values)

    def get_all_responses(self) -> Dict[str, Any]:
        return {k: dict(v) for k, v in self.responses_by_step.items()}

    def can_go_back(self) -> bool:
        return len(self.history) > 0

    def go_back(self) -> Optional[str]:
        if not self.history:
            return None
        last_step = self.history.pop()
        self.responses_by_step.pop(last_step, None)
        return self.history[-1] if self.history else None
