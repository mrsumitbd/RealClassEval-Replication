from __future__ import annotations

from dataclasses import dataclass, asdict, is_dataclass
from typing import Any
from copy import deepcopy


@dataclass
class SessionAgent:
    data: dict[str, Any]

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        if hasattr(agent, "to_dict") and callable(getattr(agent, "to_dict")):
            mapping = agent.to_dict()
            if not isinstance(mapping, dict):
                raise TypeError("Agent.to_dict() must return a dict")
            return cls(deepcopy(mapping))

        if is_dataclass(agent):
            return cls(deepcopy(asdict(agent)))

        if hasattr(agent, "__dict__"):
            mapping = {
                k: v
                for k, v in vars(agent).items()
                if not k.startswith("_") and not callable(v)
            }
            return cls(deepcopy(mapping))

        raise TypeError("Unsupported agent type for serialization")

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        if not isinstance(env, dict):
            raise TypeError("env must be a dict[str, Any]")
        return cls(deepcopy(env))

    def to_dict(self) -> dict[str, Any]:
        return deepcopy(self.data)
