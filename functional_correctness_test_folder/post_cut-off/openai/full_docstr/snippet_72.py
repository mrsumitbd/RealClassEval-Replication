
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class SessionAgent:
    """Agent that belongs to a Session."""

    # Store all attributes in a dictionary
    attributes: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_agent(cls, agent: "Agent") -> "SessionAgent":
        """
        Convert an Agent to a SessionAgent.

        All public, non-callable attributes of the given agent are copied
        into the new SessionAgent's `attributes` dictionary.
        """
        attrs = {
            name: getattr(agent, name)
            for name in dir(agent)
            if not name.startswith("_") and not callable(getattr(agent, name))
        }
        return cls(attributes=attrs)

    @classmethod
    def from_dict(cls, env: Dict[str, Any]) -> "SessionAgent":
        """
        Initialize a SessionAgent from a dictionary, ignoring keys that are not
        class parameters.

        Since SessionAgent only stores a generic `attributes` dictionary,
        all key/value pairs from the input dictionary are copied.
        """
        return cls(attributes=dict(env))

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the SessionAgent to a dictionary representation.
        """
        return dict(self.attributes)

    # Optional: allow attribute access directly
    def __getattr__(self, name: str) -> Any:
        try:
            return self.attributes[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "attributes":
            super().__setattr__(name, value)
        else:
            self.attributes[name] = value
