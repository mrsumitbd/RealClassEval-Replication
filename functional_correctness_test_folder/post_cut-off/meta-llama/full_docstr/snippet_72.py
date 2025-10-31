
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Agent:
    # Assuming Agent class has the following attributes
    id: int
    name: str


@dataclass
class SessionAgent:
    '''Agent that belongs to a Session.'''
    id: int
    name: str

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        '''Convert an Agent to a SessionAgent.'''
        return cls(id=agent.id, name=agent.name)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        '''Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters.'''
        return cls(**{k: v for k, v in env.items() if k in ['id', 'name']})

    def to_dict(self) -> dict[str, Any]:
        '''Convert the SessionAgent to a dictionary representation.'''
        return asdict(self)
