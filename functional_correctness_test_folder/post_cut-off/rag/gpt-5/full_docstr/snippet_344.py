from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Dict, List
import numpy as np


@dataclass
class OptimizationResults:
    '''
    Structured container for optimization results from the Successive Convexification (SCP) solver.
    This class provides a type-safe and organized way to store and access optimization results,
    replacing the previous dictionary-based approach. It includes core optimization data,
    iteration history for convergence analysis, post-processing results, and flexible
    storage for plotting and application-specific data.
    Attributes:
        converged (bool): Whether the optimization successfully converged
        t_final (float): Final time of the optimized trajectory
        u (Control): Optimized control trajectory at discretization nodes
        x (State): Optimized state trajectory at discretization nodes
        # SCP Iteration History (for convergence analysis)
        x_history (list[np.ndarray]): State trajectories from each SCP iteration
        u_history (list[np.ndarray]): Control trajectories from each SCP iteration
        discretization_history (list[np.ndarray]): Time discretization from each iteration
        J_tr_history (list[np.ndarray]): Trust region cost history
        J_vb_history (list[np.ndarray]): Virtual buffer cost history
        J_vc_history (list[np.ndarray]): Virtual control cost history
        # Post-processing Results (added by propagate_trajectory_results)
        t_full (Optional[np.ndarray]): Full time grid for interpolated trajectory
        x_full (Optional[np.ndarray]): Interpolated state trajectory on full time grid
        u_full (Optional[np.ndarray]): Interpolated control trajectory on full time grid
        cost (Optional[float]): Total cost of the optimized trajectory
        ctcs_violation (Optional[np.ndarray]): Continuous-time constraint violations
        # User-defined Data
        plotting_data (dict[str, Any]): Flexible storage for plotting and application data
    '''
    converged: bool = False
    t_final: Optional[float] = None
    u: Optional[Any] = None
    x: Optional[Any] = None

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
        '''Initialize the results object.'''
        # Normalize list-like fields in case None was provided explicitly
        for name in (
            'x_history', 'u_history', 'discretization_history',
            'J_tr_history', 'J_vb_history', 'J_vc_history'
        ):
            if getattr(self, name) is None:
                setattr(self, name, [])
        # Ensure plotting_data is a dict
        if self.plotting_data is None:
            self.plotting_data = {}

    def update_plotting_data(self, **kwargs):
        '''
        Update the plotting data with additional information.
        Args:
            **kwargs: Key-value pairs to add to plotting_data
        '''
        if not kwargs:
            return
        self.plotting_data.update(kwargs)

    def get(self, key: str, default: Any = None) -> Any:
        '''
        Get a value from the results, similar to dict.get().
        Args:
            key: The key to look up
            default: Default value if key is not found
        Returns:
            The value associated with the key, or default if not found
        '''
        if key in self.__dataclass_fields__:
            return getattr(self, key)
        if key in self.plotting_data:
            return self.plotting_data[key]
        return default

    def __getitem__(self, key: str) -> Any:
        '''
        Allow dictionary-style access to results.
        Args:
            key: The key to look up
        Returns:
            The value associated with the key
        Raises:
            KeyError: If key is not found
        '''
        if key in self.__dataclass_fields__:
            return getattr(self, key)
        if key in self.plotting_data:
            return self.plotting_data[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any):
        '''
        Allow dictionary-style assignment to results.
        Args:
            key: The key to set
            value: The value to assign
        '''
        if key in self.__dataclass_fields__:
            setattr(self, key, value)
        else:
            self.plotting_data[key] = value

    def __contains__(self, key: str) -> bool:
        '''
        Check if a key exists in the results.
        Args:
            key: The key to check
        Returns:
            True if key exists, False otherwise
        '''
        if key in self.plotting_data:
            return True
        if key in self.__dataclass_fields__:
            return getattr(self, key) is not None
        return False

    def update_plotting_data(self, **kwargs):
        '''
        Update the results with additional data from a dictionary.
        Args:
            other: Dictionary containing additional data
        '''
        if not kwargs:
            return
        self.plotting_data.update(kwargs)

    def to_dict(self) -> dict[str, Any]:
        '''
        Convert the results to a dictionary for backward compatibility.
        Returns:
            Dictionary representation of the results
        '''
        return asdict(self)
