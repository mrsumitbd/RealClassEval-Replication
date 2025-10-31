from __future__ import annotations

from dataclasses import dataclass, field, fields, asdict, replace, is_dataclass
from typing import Any, Dict


@dataclass
class SessionAgent:
    """Agent that belongs to a Session."""
    id: str | None = None
    name: str | None = None
    kind: str | None = None
    config: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        """Convert an Agent to a SessionAgent."""
        if isinstance(agent, SessionAgent):
            return replace(agent)

        data: Dict[str, Any] | None = None

        # Prefer an explicit to_dict implementation if available
        to_dict = getattr(agent, "to_dict", None)
        if callable(to_dict):
            try:
                data = to_dict()
            except Exception:
                data = None

        # If it's a dataclass instance, convert it to dict
        if data is None and is_dataclass(agent):
            try:
                data = asdict(agent)
            except Exception:
                data = None

        # Fallback to __dict__ (public attrs only)
        if data is None:
            obj_dict = getattr(agent, "__dict__", {})
            if isinstance(obj_dict, dict):
                data = {k: v for k, v in obj_dict.items()
                        if not k.startswith("_")}
            else:
                data = {}

        # As a last resort, try common attribute names explicitly
        if not data:
            for attr in (
                "id", "agent_id", "uuid",
                "name",
                "kind", "type", "agent_type",
                "config", "params", "parameters", "settings",
                "metadata", "meta",
            ):
                if hasattr(agent, attr):
                    data[attr] = getattr(agent, attr)

        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        """Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters."""
        if not isinstance(env, dict):
            raise TypeError("env must be a dict[str, Any]")

        # Support common aliases for fields
        aliases = {
            "agent_id": "id",
            "uuid": "id",
            "type": "kind",
            "agent_type": "kind",
            "params": "config",
            "parameters": "config",
            "settings": "config",
            "meta": "metadata",
        }

        normalized: Dict[str, Any] = {}
        for key, value in env.items():
            normalized[aliases.get(key, key)] = value

        allowed = {f.name for f in fields(cls)}
        filtered: Dict[str, Any] = {k: v for k,
                                    v in normalized.items() if k in allowed}

        # Ensure dict fields have correct types
        if "config" in filtered and not isinstance(filtered["config"], dict):
            filtered["config"] = dict(
                filtered["config"]) if filtered["config"] is not None else {}
        if "metadata" in filtered and not isinstance(filtered["metadata"], dict):
            filtered["metadata"] = dict(
                filtered["metadata"]) if filtered["metadata"] is not None else {}

        return cls(**filtered)

    def to_dict(self) -> dict[str, Any]:
        """Convert the SessionAgent to a dictionary representation."""
        return asdict(self)
