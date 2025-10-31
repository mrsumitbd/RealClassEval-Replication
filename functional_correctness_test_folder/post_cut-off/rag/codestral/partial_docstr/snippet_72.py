
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SessionAgent:
    '''Agent that belongs to a Session.'''
    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        '''Convert an Agent to a SessionAgent.'''
        return cls(**agent.__dict__)

    @classmethod
    def from_dict(cls, env: Dict[str, Any]) -> 'SessionAgent':
        '''Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters.'''
        params = {k: v for k, v in env.items() if k in cls.__annotations__}
        return cls(**params)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the SessionAgent to a dictionary representation.'''
        return self.__dict__
