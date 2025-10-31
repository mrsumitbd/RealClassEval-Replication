
from dataclasses import dataclass, fields
from typing import Any, Dict


@dataclass
class SessionAgent:

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        '''Convert an Agent to a SessionAgent.'''
        # Assuming Agent has the same fields as SessionAgent
        return cls(**{field.name: getattr(agent, field.name) for field in fields(cls)})

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        '''Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters.'''
        return cls(**{field.name: env[field.name] for field in fields(cls) if field.name in env})

    def to_dict(self) -> dict[str, Any]:
        '''Convert the SessionAgent to a dictionary representation.'''
        return {field.name: getattr(self, field.name) for field in fields(self)}
