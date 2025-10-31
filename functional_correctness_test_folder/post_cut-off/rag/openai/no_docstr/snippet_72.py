
from __future__ import annotations
from dataclasses import dataclass, fields
from typing import Any, Dict, Type, TypeVar

T = TypeVar('T', bound='SessionAgent')


@dataclass
class SessionAgent:
    '''Agent that belongs to a Session.'''

    @classmethod
    def from_agent(cls: Type[T], agent: Any) -> T:
        '''Convert an Agent to a SessionAgent.'''
        # Build a dict of attributes that exist on the agent and are
        # defined as dataclass fields on SessionAgent.
        field_names = {f.name for f in fields(cls)}
        data = {name: getattr(agent, name)
                for name in field_names if hasattr(agent, name)}
        return cls(**data)

    @classmethod
    def from_dict(cls: Type[T], env: Dict[str, Any]) -> T:
        '''Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters.'''
        field_names = {f.name for f in fields(cls)}
        data = {name: env[name] for name in field_names if name in env}
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the SessionAgent to a dictionary representation.'''
        return {f.name: getattr(self, f.name) for f in fields(self)}
