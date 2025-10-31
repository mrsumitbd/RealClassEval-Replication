
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SessionAgent:

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        return cls()

    @classmethod
    def from_dict(cls, env: Dict[str, Any]) -> 'SessionAgent':
        return cls()

    def to_dict(self) -> Dict[str, Any]:
        return {}
