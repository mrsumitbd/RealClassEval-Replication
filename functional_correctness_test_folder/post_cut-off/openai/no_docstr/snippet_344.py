
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class OptimizationResults:
    """
    A simple container for optimization results that behaves like a dictionary
    and also keeps a separate dictionary for data used in plotting.
    """

    # Internal storage for arbitrary key/value pairs
    _data: Dict[str, Any] = field(default_factory=dict, init=False, repr=False)
    # Storage for plotting‑specific data
    _plotting_data: Dict[str, Any] = field(
        default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        """
        Ensure that the internal dictionaries are always present.
        """
        # The default_factory already creates the dicts, but this guard
        # protects against accidental manual overrides.
        if not isinstance(self._data, dict):
            self._data = {}
        if not isinstance(self._plotting_data, dict):
            self._plotting_data = {}

    # ------------------------------------------------------------------
    # Dictionary‑like interface for the main data
    # ------------------------------------------------------------------
    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for *key* if it exists, otherwise *default*."""
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Allow dictionary‑style access: results[key]."""
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Allow dictionary‑style assignment: results[key] = value."""
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        """Allow use of the 'in' operator."""
        return key in self._data

    # ------------------------------------------------------------------
    # Plotting data handling
    # ------------------------------------------------------------------
    def update_plotting_data(self, **kwargs: Any) -> None:
        """
        Update the internal plotting data dictionary with the provided keyword
        arguments. Existing keys are overwritten.
        """
        self._plotting_data.update(kwargs)

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """
        Return a shallow copy of the main data dictionary.
        """
        return dict(self._data)

    # ------------------------------------------------------------------
    # Convenience accessors for plotting data
    # ------------------------------------------------------------------
    @property
    def plotting_data(self) -> Dict[str, Any]:
        """Read‑only access to the plotting data dictionary."""
        return dict(self._plotting_data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"
