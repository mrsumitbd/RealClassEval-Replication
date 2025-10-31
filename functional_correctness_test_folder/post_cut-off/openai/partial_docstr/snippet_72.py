
from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="SessionAgent")


@dataclass
class SessionAgent:
    """
    A lightweight representation of an Agent that can be serialised to/from
    dictionaries and constructed from an existing Agent instance.
    """

    @classmethod
    def from_agent(cls: Type[T], agent: Any) -> T:
        """
        Create a SessionAgent from an arbitrary Agent instance.

        Parameters
        ----------
        agent : Any
            The source Agent object.  Only attributes that match the field
            names of the SessionAgent dataclass are copied.

        Returns
        -------
        SessionAgent
            A new SessionAgent instance populated with matching attributes.
        """
        if not is_dataclass(agent):
            # If the agent is not a dataclass, fall back to attribute lookup.
            agent_dict = {k: getattr(agent, k)
                          for k in dir(agent) if not k.startswith("_")}
        else:
            agent_dict = {f.name: getattr(agent, f.name)
                          for f in fields(agent)}

        # Filter keys that are valid fields for SessionAgent
        valid_keys = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in agent_dict.items() if k in valid_keys}
        return cls(**filtered)  # type: ignore[arg-type]

    @classmethod
    def from_dict(cls: Type[T], env: Dict[str, Any]) -> T:
        """
        Initialise a SessionAgent from a dictionary, ignoring keys that are
        not defined as dataclass fields.

        Parameters
        ----------
        env : dict[str, Any]
            Dictionary containing potential field values.

        Returns
        -------
        SessionAgent
            A new SessionAgent instance with fields populated from the dict.
        """
        valid_keys = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in env.items() if k in valid_keys}
        return cls(**filtered)  # type: ignore[arg-type]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the SessionAgent instance into a plain dictionary.

        Returns
        -------
        dict[str, Any]
            Dictionary representation of the SessionAgent.
        """
        return {f.name: getattr(self, f.name) for f in fields(self)}
