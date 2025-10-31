
from dataclasses import dataclass, field
from typing import Any, Dict, Set


@dataclass
class OverridableConfig:
    """
    A simple configuration holder that tracks which keys have been overridden.
    The actual configuration values are stored in the instance's __dict__.
    """

    # Optional: store default values for keys (if desired)
    _defaults: Dict[str, Any] = field(
        default_factory=dict, init=False, repr=False)
    # Set of keys that have been overridden
    _overridden_keys: Set[str] = field(
        default_factory=set, init=False, repr=False)

    def __post_init__(self) -> None:
        """
        Initialize the overridden keys set after dataclass initialization.
        """
        self._overridden_keys = set()

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        """
        Mark a configuration key as overridden or reset it to its default.

        Parameters
        ----------
        key : str
            The configuration key to modify.
        reset_to_defaults : bool, default True
            If True, the key is removed from the overridden set (i.e., reset to default).
            If False, the key is added to the overridden set.
        """
        if reset_to_defaults:
            self._overridden_keys.discard(key)
        else:
            self._overridden_keys.add(key)

    # Optional helper methods for convenience

    def is_overridden(self, key: str) -> bool:
        """
        Check if a key is currently overridden.

        Parameters
        ----------
        key : str
            The configuration key to check.

        Returns
        -------
        bool
            True if the key is overridden, False otherwise.
        """
        return key in self._overridden_keys

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a configuration value, falling back to the default if not set.

        Parameters
        ----------
        key : str
            The configuration key to retrieve.
        default : Any, optional
            The value to return if the key is not present.

        Returns
        -------
        Any
            The configuration value or the provided default.
        """
        return getattr(self, key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value and mark it as overridden.

        Parameters
        ----------
        key : str
            The configuration key to set.
        value : Any
            The value to assign to the key.
        """
        setattr(self, key, value)
        self._overridden_keys.add(key)

    def reset_to_defaults(self) -> None:
        """
        Reset all overridden keys to their default values (if defaults are defined).
        """
        for key in list(self._overridden_keys):
            if key in self._defaults:
                setattr(self, key, self._defaults[key])
            else:
                # If no default is defined, simply delete the attribute
                if hasattr(self, key):
                    delattr(self, key)
            self._overridden_keys.discard(key)
