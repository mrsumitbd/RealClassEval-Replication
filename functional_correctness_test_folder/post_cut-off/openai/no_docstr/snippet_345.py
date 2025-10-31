
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EnhancedUser:
    """
    A lightweight wrapper around a user dictionary that provides convenient
    access to common fields such as the user ID.
    """
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnhancedUser":
        """
        Create an EnhancedUser instance from a plain dictionary.

        Parameters
        ----------
        data : Dict[str, Any]
            The raw user data.

        Returns
        -------
        EnhancedUser
            A new instance containing the supplied data.
        """
        # Ensure we store a copy to avoid accidental mutation of the caller's dict
        return cls(data=dict(data))

    def get_user_id(self) -> Optional[str]:
        """
        Retrieve the user ID from the underlying data.

        The method looks for common key names that might hold the ID:
        'id', 'user_id', or 'userId'.

        Returns
        -------
        Optional[str]
            The user ID if present, otherwise None.
        """
        for key in ("id", "user_id", "userId"):
            if key in self.data:
                return str(self.data[key])
        return None
