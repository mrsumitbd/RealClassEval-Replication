from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class GeneratedScenario:
    """A single scenario for testing AI agents."""
    task: str
    difficulty: int

    def __post_init__(self):
        if not isinstance(self.difficulty, int) or not 1 <= self.difficulty <= 5:
            raise ValueError('Difficulty must be an integer between 1 and 5')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GeneratedScenario':
        """Create a GeneratedScenario from a dictionary."""
        return cls(task=data['task'], difficulty=data['difficulty'])

    def to_dict(self) -> Dict[str, Any]:
        """Convert the scenario to a dictionary."""
        return {'task': self.task, 'difficulty': self.difficulty}

    def preview(self, max_length: int=120) -> str:
        """Get a preview of the scenario task."""
        if len(self.task) <= max_length:
            return self.task
        return self.task[:max_length].strip() + '…'