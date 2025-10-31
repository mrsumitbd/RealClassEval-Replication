
from dataclasses import dataclass, fields
from typing import Any


@dataclass
class SessionAgent:
    '''Agent that belongs to a Session.'''
    id: int = 0
    name: str = ""
    role: str = ""

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        '''Convert an Agent to a SessionAgent.'''
        params = {f.name: getattr(agent, f.name, None) for f in fields(cls)}
        return cls(**params)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        '''Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters.'''
        params = {f.name: env[f.name] for f in fields(cls) if f.name in env}
        return cls(**params)

    def to_dict(self) -> dict[str, Any]:
        '''Convert the SessionAgent to a dictionary representation.'''
        return {f.name: getattr(self, f.name) for f in fields(self)}
