
from dataclasses import dataclass, fields
from typing import Any, Dict


@dataclass
class SessionAgent:
    '''Agent that belongs to a Session.'''
    agent_id: str
    session_id: str
    active: bool = True

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        '''Convert an Agent to a SessionAgent.'''
        return cls(agent_id=agent.agent_id, session_id=agent.session_id, active=agent.active)

    @classmethod
    def from_dict(cls, env: Dict[str, Any]) -> 'SessionAgent':
        '''Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters.'''
        field_names = {field.name for field in fields(cls)}
        filtered_env = {key: value for key,
                        value in env.items() if key in field_names}
        return cls(**filtered_env)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the SessionAgent to a dictionary representation.'''
        return {field.name: getattr(self, field.name) for field in fields(self)}
