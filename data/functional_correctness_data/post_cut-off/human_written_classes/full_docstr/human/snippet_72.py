import inspect
from typing import TYPE_CHECKING, Any, Dict, Optional
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

@dataclass
class SessionAgent:
    """Agent that belongs to a Session."""
    agent_id: str
    state: Dict[str, Any]
    conversation_manager_state: Dict[str, Any]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        """Convert an Agent to a SessionAgent."""
        if agent.agent_id is None:
            raise ValueError('agent_id needs to be defined.')
        return cls(agent_id=agent.agent_id, conversation_manager_state=agent.conversation_manager.get_state(), state=agent.state.get())

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        """Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters."""
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})

    def to_dict(self) -> dict[str, Any]:
        """Convert the SessionAgent to a dictionary representation."""
        return asdict(self)