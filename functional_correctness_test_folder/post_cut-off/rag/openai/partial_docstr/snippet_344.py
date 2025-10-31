
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class OptimizationResults:
    """
    Structured container for optimization results from the Successive Convexification (SCP) solver.
    This class provides a type-safe and organized way to store and access optimization results,
    replacing the previous dictionary-based approach. It includes core optimization data,
    iteration history for convergence analysis, post-processing results, and flexible
    storage for plotting and application-specific data.
    """

    # Core optimization data
    converged: bool = False
    t_final: float = 0.0
    u: Any = None  # Optimized control trajectory
    x: Any = None  # Optimized state trajectory

    # SCP Iteration History
    x_history: List[np.ndarray] = field(default_factory=list)
    u_history: List[np.ndarray] = field(default_factory=list)
    discretization_history: List[np.ndarray] = field(default_factory=list)
    J_tr_history: List[np.ndarray] = field(default_factory=list)
    J_vb_history: List[np.ndarray] = field(default_factory=list)
    J_vc_history: List[np.ndarray] = field(default_factory=list)

    # Post-processing Results
    t_full: Optional[np.ndarray] = None
    x_full: Optional[np.ndarray] = None
    u_full: Optional[np.ndarray] = None
    cost: Optional[float] = None
    ctcs_violation: Optional[np.ndarray] = None

    # User-defined Data
    plotting_data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Ensure that plotting_data is a dictionary."""
        if self.plotting_data is None:
            self.plotting_data = {}
        elif not isinstance(self.plotting_data, dict):
            raise TypeError(
                f"plotting_data must be a dict, got {type(self.plotting_data).__name__}"
            )

    # ------------------------------------------------------------------
    # Dictionary-like interface
    # ------------------------------------------------------------------
    def update_plotting_data(self, **kwargs):
        """
        Update the plotting data with additional information.
        Args:
            **kwargs: Key-value pairs to add to plotting_data
        """
        self.plotting_data.update(kwargs)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the results, similar to dict.get().
        Args:
            key: The key to look up
            default: Default value if key is not found
        Returns:
            The value associated with the key, or default if not found
        """
        if hasattr(self, key):
            return getattr(self, key)
        return self.plotting_data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """
        Allow dictionary-style access to results.
        Args:
            key: The key to look up
        Returns:
            The value associated with the key
        Raises:
            KeyError: If key is not found
        """
        if hasattr(self, key):
            return getattr(self, key)
        if key in self.plotting_data:
            return self.plotting_data[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any):
        """
        Allow dictionary-style assignment to results.
        Args:
            key: The key to set
            value: The value to assign
        """
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.plotting_data[key] = value

    def __contains__(self, key: str) -> bool:
        """
        Check if a key exists in the results.
        Args:
            key: The key to check
        Returns:
            True if key exists, False otherwise
        """
        return hasattr(self, key) or key in self.plotting_data

    # ------------------------------------------------------------------
    # Additional helper methods
    # ------------------------------------------------------------------
    def update_plotting_data_from_dict(self, other: Dict[str, Any]):
        """
        Update the results with additional data from a dictionary.
        Args:
            other: Dictionary containing additional data
        """
        if not isinstance(other, dict):
            raise TypeError(f"Expected dict, got {type(other).__name__}")
        self.plotting_data.update(other)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the results to a dictionary for backward compatibility.
        Returns:
            Dictionary representation of the results
        """
        # Use asdict to get all fields, then merge with plotting_data
        d = asdict(self)
        # plotting_data is already part of d, but ensure it's a plain dict
        d["plotting_data"] = dict(d.get("plotting_data", {}))
        return d
