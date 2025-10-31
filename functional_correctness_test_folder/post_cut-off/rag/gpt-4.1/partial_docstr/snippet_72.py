from dataclasses import dataclass, fields
from typing import Any


@dataclass
class SessionAgent:
    """Agent that belongs to a Session."""
    id: str
    name: str
    role: str

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        """Convert an Agent to a SessionAgent."""
        return cls(id=agent.id, name=agent.name, role=agent.role)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        """Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters."""
        field_names = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in env.items() if k in field_names}
        return cls(**filtered)

    def to_dict(self) -> dict[str, Any]:
        """Convert the SessionAgent to a dictionary representation."""
        return {f.name: getattr(self, f.name) for f in fields(self)}
