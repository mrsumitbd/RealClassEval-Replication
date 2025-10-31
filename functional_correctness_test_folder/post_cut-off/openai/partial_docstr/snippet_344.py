
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
    u: Any = None  # Control trajectory (np.ndarray or custom type)
    x: Any = None  # State trajectory (np.ndarray or custom type)

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
        """Ensure that mutable defaults are properly initialized."""
        # The default_factory already handles list/dict creation,
        # but we guard against accidental shared references.
        if self.plotting_data is None:
            self.plotting_data = {}

    # ------------------------------------------------------------------
    # Dictionary-like interface
    # ------------------------------------------------------------------
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the results, similar to dict.get()."""
        return getattr(self, key, default)

    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access to results."""
        if not hasattr(self, key):
            raise KeyError(f"'{key}' not found in OptimizationResults")
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Allow dictionary-style assignment to results."""
        setattr(self, key, value)

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the results."""
        return hasattr(self, key)

    # ------------------------------------------------------------------
    # Plotting data utilities
    # ------------------------------------------------------------------
    def update_plotting_data(self, **kwargs: Any) -> None:
        """
        Update the results with additional data from keyword arguments.
        """
        for k, v in kwargs.items():
            self.plotting_data[k] = v

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the results to a dictionary for backward compatibility.
        """
        # Use asdict to recursively convert dataclass fields.
        # Convert numpy arrays to lists for JSON serializability if needed.
        def _convert(value: Any) -> Any:
            if isinstance(value, np.ndarray):
                return value.tolist()
            if isinstance(value, (list, tuple)):
                return [_convert(v) for v in value]
            if isinstance(value, dict):
                return {k: _convert(v) for k, v in value.items()}
            return value

        raw_dict = asdict(self)
        return {k: _convert(v) for k, v in raw_dict.items()}
