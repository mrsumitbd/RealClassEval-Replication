
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class RegistryConfig:
    """
    A simple dataclass that can hold arbitrary configuration data.
    The class provides convenient methods to convert the instance to a
    dictionary and to produce readable string representations.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Return a dictionary representation of the instance.
        All attributes stored in the instance's __dict__ are included.
        """
        return dict(self.__dict__)

    def __repr__(self) -> str:
        """
        Return an unambiguous string representation of the instance.
        """
        return f"{self.__class__.__name__}({self.__dict__!r})"

    def __str__(self) -> str:
        """
        Return a readable string representation of the instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"
