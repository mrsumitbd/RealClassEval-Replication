
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Union

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
    t_final: Optional[float] = None
    u: Optional[np.ndarray] = None
    x: Optional[np.ndarray] = None

    # SCP Iteration History (for convergence analysis)
    x_history: List[np.ndarray] = field(default_factory=list)
    u_history: List[np.ndarray] = field(default_factory=list)
    discretization_history: List[np.ndarray] = field(default_factory=list)
    J_tr_history: List[np.ndarray] = field(default_factory=list)
    J_vb_history: List[np.ndarray] = field(default_factory=list)
    J_vc_history: List[np.ndarray] = field(default_factory=list)

    # Post-processing Results (added by propagate_trajectory_results)
    t_full: Optional[np.ndarray] = None
    x_full: Optional[np.ndarray] = None
    u_full: Optional[np.ndarray] = None
    cost: Optional[float] = None
    ctcs_violation: Optional[np.ndarray] = None

    # User-defined Data
    plotting_data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Ensure that history containers are lists and plotting_data is a dict."""
        # The default_factory already guarantees lists/dict, but we guard against None.
        if self.x_history is None:
            self.x_history = []
        if self.u_history is None:
            self.u_history = []
        if self.discretization_history is None:
            self.discretization_history = []
        if self.J_tr_history is None:
            self.J_tr_history = []
        if self.J_vb_history is None:
            self.J_vb_history = []
        if self.J_vc_history is None:
            self.J_vc_history = []
        if self.plotting_data is None:
            self.plotting_data = {}

    # ------------------------------------------------------------------
    # Dictionary-like interface
    # ------------------------------------------------------------------
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the results, similar to dict.get()."""
        if hasattr(self, key):
            return getattr(self, key)
        return default

    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access to results."""
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"'{key}' not found in OptimizationResults")

    def __setitem__(self, key: str, value: Any) -> None:
        """Allow dictionary-style assignment to results."""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            # If the key does not exist, create a new attribute
            setattr(self, key, value)

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the results."""
        return hasattr(self, key)

    # ------------------------------------------------------------------
    # Plotting data utilities
    # ------------------------------------------------------------------
    def update_plotting_data(self, **kwargs: Any) -> None:
        """
        Update the plotting data with additional information.
        Args:
            **kwargs: Key-value pairs to add to plotting_data
        """
        self.plotting_data.update(kwargs)

    # ------------------------------------------------------------------
    # Backward compatibility
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the results to a dictionary for backward compatibility.
        Returns:
            Dictionary representation of the results
        """
        # Use asdict to recursively convert dataclass fields.
        return asdict(self)
