
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class SessionAgent:
    """A lightweight wrapper that stores session‑related data extracted from an Agent."""

    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_agent(cls, agent: "Agent") -> "SessionAgent":
        """
        Create a SessionAgent instance from an Agent object.

        The agent is converted to a plain dictionary using its ``__dict__`` attribute.
        """
        # Use vars() to get the agent's attribute dictionary.
        agent_dict = vars(agent)
        return cls(data=dict(agent_dict))

    @classmethod
    def from_dict(cls, env: Dict[str, Any]) -> "SessionAgent":
        """
        Create a SessionAgent instance from a dictionary.

        The dictionary is stored directly as the internal data representation.
        """
        return cls(data=dict(env))

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the internal data dictionary.

        This method provides a serialisable representation of the session agent.
        """
        return dict(self.data)
