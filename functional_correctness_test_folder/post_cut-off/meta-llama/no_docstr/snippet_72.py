
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class SessionAgent:
    # Assuming Agent is defined elsewhere in the codebase
    # For demonstration purposes, we'll define a simple Agent class
    # In a real scenario, you should import or define Agent accordingly
    class Agent:
        def __init__(self, id: str, name: str):
            self.id = id
            self.name = name

    id: str
    name: str

    @classmethod
    def from_agent(cls, agent: 'SessionAgent.Agent') -> 'SessionAgent':
        return cls(id=agent.id, name=agent.name)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        return cls(**env)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
