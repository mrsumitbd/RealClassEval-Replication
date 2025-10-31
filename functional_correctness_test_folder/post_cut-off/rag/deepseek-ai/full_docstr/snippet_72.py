
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class SessionAgent:
    """Agent that belongs to a Session."""

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        """Convert an Agent to a SessionAgent."""
        return cls(**agent.__dict__)

    @classmethod
    def from_dict(cls, env: Dict[str, Any]) -> 'SessionAgent':
        """Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters."""
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_env = {k: v for k, v in env.items() if k in valid_fields}
        return cls(**filtered_env)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the SessionAgent to a dictionary representation."""
        return asdict(self)
