
from dataclasses import dataclass, fields
from typing import Any, Dict


@dataclass
class SessionAgent:
    '''Agent that belongs to a Session.'''
    # Assuming some fields for the SessionAgent, as they are not specified
    agent_id: int
    session_id: int
    name: str

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        '''Convert an Agent to a SessionAgent.'''
        return cls(agent_id=agent.agent_id, session_id=agent.session_id, name=agent.name)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        '''Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters.'''
        return cls(**{field.name: env.get(field.name) for field in fields(cls)})

    def to_dict(self) -> dict[str, Any]:
        '''Convert the SessionAgent to a dictionary representation.'''
        return {field.name: getattr(self, field.name) for field in fields(self)}
