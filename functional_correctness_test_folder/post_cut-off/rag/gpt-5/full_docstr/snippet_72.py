from dataclasses import dataclass, field, fields, asdict, is_dataclass
from typing import Any, Optional, Mapping


@dataclass
class SessionAgent:
    """Agent that belongs to a Session."""
    agent_id: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    config: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_agent(cls, agent: 'Agent') -> 'SessionAgent':
        """Convert an Agent to a SessionAgent."""
        data: dict[str, Any] = {}

        if isinstance(agent, Mapping):
            data = dict(agent)
        elif hasattr(agent, 'to_dict') and callable(getattr(agent, 'to_dict')):
            try:
                maybe = agent.to_dict()
                if isinstance(maybe, Mapping):
                    data = dict(maybe)
            except Exception:
                data = {}
        elif is_dataclass(agent):
            try:
                data = asdict(agent)
            except Exception:
                data = {}

        def get_from_sources(keys: tuple[str, ...], default: Any = None) -> Any:
            for k in keys:
                if isinstance(data, Mapping) and k in data and data[k] is not None:
                    return data[k]
                if hasattr(agent, k):
                    v = getattr(agent, k)
                    if v is not None:
                        return v
            return default

        agent_id = get_from_sources(('agent_id', 'id', 'uuid', 'identifier'))
        name = get_from_sources(('name', 'display_name', 'title'))
        role = get_from_sources(('role', 'type'))
        cfg = get_from_sources(
            ('config', 'params', 'settings', 'metadata', 'extra'), {}) or {}
        if not isinstance(cfg, dict):
            try:
                cfg = dict(cfg)  # type: ignore[arg-type]
            except Exception:
                cfg = {'value': cfg}

        return cls(agent_id=agent_id, name=name, role=role, config=cfg)

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> 'SessionAgent':
        """Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters."""
        allowed = {f.name for f in fields(cls)}
        kwargs = {k: v for k, v in (env or {}).items() if k in allowed}
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the SessionAgent to a dictionary representation."""
        result: dict[str, Any] = {}
        for f in fields(self):
            val = getattr(self, f.name)
            if val is None:
                continue
            if isinstance(val, dict) and not val:
                continue
            result[f.name] = val
        return result
