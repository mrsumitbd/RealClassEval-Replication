
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="SessionAgent")


@dataclass
class SessionAgent:
    """Agent that belongs to a Session."""

    @classmethod
    def from_agent(cls: Type[T], agent: Any) -> T:
        """Convert an Agent to a SessionAgent."""
        # Copy only attributes that are defined as dataclass fields
        field_names = {f.name for f in fields(cls)}
        kwargs = {name: getattr(agent, name)
                  for name in field_names if hasattr(agent, name)}
        return cls(**kwargs)

    @classmethod
    def from_dict(cls: Type[T], env: Dict[str, Any]) -> T:
        """Initialize a SessionAgent from a dictionary, ignoring keys that are not class parameters."""
        field_names = {f.name for f in fields(cls)}
        kwargs = {name: env[name] for name in field_names if name in env}
        return cls(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the SessionAgent to a dictionary representation."""
        return {f.name: getattr(self, f.name) for f in fields(self)}
