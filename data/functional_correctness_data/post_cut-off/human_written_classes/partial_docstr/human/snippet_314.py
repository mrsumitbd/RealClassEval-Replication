from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

@dataclass
class SimpleFunction:
    """Ultra-simplified function wrapper."""
    name: str
    entrypoint: Callable
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {'type': 'object', 'properties': {}, 'required': []}

    def to_dict(self) -> Dict[str, Any]:
        """Convert function to dictionary."""
        return {'name': self.name, 'description': self.description, 'parameters': self.parameters}

    def execute(self, **kwargs) -> Any:
        """Execute the function with given arguments."""
        return self.entrypoint(**kwargs)