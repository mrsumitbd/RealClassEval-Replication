from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Protocol

    class Agent(Protocol):
        def to_dict(self) -> Dict[str, Any]: ...
        # Fallback to attribute dict if to_dict is not implemented


@dataclass
class SessionAgent:
    name: Optional[str] = None
    role: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    extras: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        data: Dict[str, Any]
        if hasattr(agent, "to_dict") and callable(getattr(agent, "to_dict")):
            data = agent.to_dict()  # type: ignore[assignment]
        else:
            data = {k: v for k, v in vars(
                agent).items() if not k.startswith("_")}
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        if not isinstance(env, dict):
            raise TypeError("env must be a dictionary")
        # type: ignore[attr-defined]
        field_names = set(f.name for f in cls.__dataclass_fields__.values())
        known: Dict[str, Any] = {}
        extras: Dict[str, Any] = {}
        for k, v in env.items():
            if k in field_names:
                known[k] = v
            else:
                extras[k] = v
        # Ensure extras are merged if provided directly
        if "extras" in known and isinstance(known["extras"], dict):
            # merge extras: env extras take precedence
            merged = {**known["extras"], **extras}
            known["extras"] = merged
        else:
            known["extras"] = extras
        return cls(**known)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
