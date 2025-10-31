from __future__ import annotations

from dataclasses import dataclass, field, asdict, is_dataclass
from typing import Any, Mapping


@dataclass
class SessionAgent:
    '''Agent that belongs to a Session.'''
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        '''Convert an Agent to a SessionAgent.'''
        extracted: dict[str, Any] = {}

        if is_dataclass(agent):
            extracted = asdict(agent)
        elif hasattr(agent, "to_dict") and callable(getattr(agent, "to_dict")):
            maybe = agent.to_dict()
            if isinstance(maybe, Mapping):
                extracted = dict(maybe)
            else:
                extracted = {"value": maybe}
        elif isinstance(agent, Mapping):
            extracted = dict(agent)
        else:
            try:
                attrs = vars(agent)
            except TypeError:
                attrs = {}
            extracted = {
                k: v
                for k, v in attrs.items()
                if not k.startswith("_") and not callable(v)
            }

        return cls(data=extracted)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        '''Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters.'''
        params: dict[str, Any] = {}
        fields = set(getattr(cls, "__dataclass_fields__", {}).keys())

        for k in env:
            if k in fields:
                params[k] = env[k]

        if "data" not in params:
            # If no explicit 'data' provided, but env looks like raw payload, store it as data
            # while respecting the "ignore non-parameters" rule for constructor.
            params["data"] = dict(env)

        # Ensure data is a dict
        if not isinstance(params.get("data"), Mapping):
            params["data"] = {"value": params.get("data")}

        return cls(**params)

    def to_dict(self) -> dict[str, Any]:
        '''Convert the SessionAgent to a dictionary representation.'''
        return dict(self.data)
