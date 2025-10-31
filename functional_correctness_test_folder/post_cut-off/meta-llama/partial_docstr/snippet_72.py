
from dataclasses import dataclass, asdict, fields
from typing import Any


@dataclass
class SessionAgent:
    # Assuming Agent is defined elsewhere
    # For demonstration purposes, let's assume Agent is also a dataclass
    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        return cls(**asdict(agent))

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        class_fields = {f.name for f in fields(cls)}
        filtered_env = {k: v for k, v in env.items() if k in class_fields}
        return cls(**filtered_env)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
