
from __future__ import annotations

from dataclasses import dataclass, fields, asdict
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="SessionAgent")


@dataclass
class SessionAgent:
    """Agent that belongs to a Session."""

    @classmethod
    def from_agent(cls: Type[T], agent: Any) -> T:
        """
        Convert an :class:`Agent` to a :class:`SessionAgent`.

        Only attributes that are defined as dataclass fields on
        :class:`SessionAgent` are copied.  Any additional attributes
        present on ``agent`` are ignored.
        """
        field_names = {f.name for f in fields(cls)}
        init_kwargs = {
            name: getattr(agent, name)
            for name in field_names
            if hasattr(agent, name)
        }
        return cls(**init_kwargs)  # type: ignore[arg-type]

    @classmethod
    def from_dict(cls: Type[T], env: Dict[str, Any]) -> T:
        """
        Initialize a :class:`SessionAgent` from a dictionary,
        ignoring keys that are not class parameters.
        """
        field_names = {f.name for f in fields(cls)}
        init_kwargs = {k: v for k, v in env.items() if k in field_names}
        return cls(**init_kwargs)  # type: ignore[arg-type]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the :class:`SessionAgent` to a dictionary representation.
        """
        return asdict(self)
