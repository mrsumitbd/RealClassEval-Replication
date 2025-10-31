
from dataclasses import dataclass
from typing import Any


@dataclass
class SessionAgent:

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        return cls()

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        return cls()

    def to_dict(self) -> dict[str, Any]:
        return {}
