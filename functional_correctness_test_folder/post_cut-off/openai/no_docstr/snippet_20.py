
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict
import copy


@dataclass
class MCPResource:
    """
    A generic resource that stores arbitrary key/value pairs.
    """
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPResource":
        """
        Create an MCPResource instance from a dictionary.

        Parameters
        ----------
        data : Dict[str, Any]
            The dictionary to initialize the resource with.

        Returns
        -------
        MCPResource
            A new instance containing a deep copy of the provided data.
        """
        # Use deepcopy to avoid accidental mutation of the original dict
        return cls(data=copy.deepcopy(data))

    def to_dict(self) -> Dict[str, Any]:
        """
        Return a deep copy of the resource's data dictionary.

        Returns
        -------
        Dict[str, Any]
            A copy of the internal data dictionary.
        """
        return copy.deepcopy(self.data)
