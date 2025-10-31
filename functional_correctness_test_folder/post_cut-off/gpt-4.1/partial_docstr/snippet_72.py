
from dataclasses import dataclass, fields
from typing import Any


@dataclass
class SessionAgent:
    id: int = 0
    name: str = ""
    session_token: str = ""
    is_active: bool = True

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        kwargs = {}
        for f in fields(cls):
            if hasattr(agent, f.name):
                kwargs[f.name] = getattr(agent, f.name)
        return cls(**kwargs)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        valid_keys = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in env.items() if k in valid_keys}
        return cls(**filtered)

    def to_dict(self) -> dict[str, Any]:
        return {f.name: getattr(self, f.name) for f in fields(self)}
