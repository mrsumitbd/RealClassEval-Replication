from dataclasses import dataclass, field, fields as dataclass_fields
from typing import Any, Optional, Dict


@dataclass
class SessionAgent:
    """Agent that belongs to a Session."""
    id: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        """Convert an Agent to a SessionAgent."""
        data: Dict[str, Any] = {}
        if hasattr(agent, 'to_dict') and callable(getattr(agent, 'to_dict')):
            try:
                data = agent.to_dict()  # type: ignore[assignment]
            except Exception:
                data = {}
        if not data and hasattr(agent, '__dict__'):
            data = dict(agent.__dict__)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        """Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters."""
        allowed = {f.name for f in dataclass_fields(cls)}
        kwargs = {k: v for k, v in env.items() if k in allowed}
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the SessionAgent to a dictionary representation."""
        return {f.name: getattr(self, f.name) for f in dataclass_fields(self)}
