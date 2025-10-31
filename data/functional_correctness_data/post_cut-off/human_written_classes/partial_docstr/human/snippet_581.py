from dataclasses import dataclass
from openscvx.backend.control import Control
from typing import Callable, Optional
from openscvx.backend.state import State
import numpy as np

@dataclass(init=False)
class SimConfig:

    def __init__(self, x: State, x_prop: State, u: Control, total_time: float, idx_x_true: slice, idx_x_true_prop: slice, idx_u_true: slice, idx_t: slice, idx_y: slice, idx_y_prop: slice, idx_s: slice, save_compiled: bool=True, ctcs_node_intervals: Optional[list]=None, constraints_ctcs: Optional[list[Callable]]=None, constraints_nodal: Optional[list[Callable]]=None, n_states: Optional[int]=None, n_states_prop: Optional[int]=None, n_controls: Optional[int]=None, scaling_x_overrides: Optional[list]=None, scaling_u_overrides: Optional[list]=None):
        """
        Configuration class for simulation settings.

        This class defines the parameters required for simulating a trajectory
        optimization problem.

        Main arguments:
        These are the arguments most commonly used day-to-day.

        Args:
            x (State): State object, must have .min and .max attributes for bounds.
            x_prop (State): Propagation state object, must have .min and .max
                attributes for bounds.
            u (Control): Control object, must have .min and .max attributes for
                bounds.
            total_time (float): The total simulation time.
            idx_x_true (slice): Slice for true state indices.
            idx_x_true_prop (slice): Slice for true propagation state indices.
            idx_u_true (slice): Slice for true control indices.
            idx_t (slice): Slice for time index.
            idx_y (slice): Slice for constraint violation indices.
            idx_y_prop (slice): Slice for propagation constraint violation
                indices.
            idx_s (slice): Slice for time dilation index.
            save_compiled (bool): If True, save and reuse compiled solver
                functions. Defaults to True.
            ctcs_node_intervals (list, optional): Node intervals for CTCS
                constraints.
            constraints_ctcs (list, optional): List of CTCS constraints.
            constraints_nodal (list, optional): List of nodal constraints.
            n_states (int, optional): The number of state variables. Defaults to
                `None` (inferred from x.max).
            n_states_prop (int, optional): The number of propagation state
                variables. Defaults to `None` (inferred from x_prop.max).
            n_controls (int, optional): The number of control variables. Defaults
                to `None` (inferred from u.max).
            scaling_x_overrides (list, optional): List of (upper_bound,
                lower_bound, idx) for custom state scaling. Each can be scalar or
                array, idx can be int, list, or slice.
            scaling_u_overrides (list, optional): List of (upper_bound,
                lower_bound, idx) for custom control scaling. Each can be scalar
                or array, idx can be int, list, or slice.

        Note:
            You can specify custom scaling for specific states/controls using
            scaling_x_overrides and scaling_u_overrides. Any indices not covered
            by overrides will use the default min/max bounds.
        """
        self.x = x
        self.x_prop = x_prop
        self.u = u
        self.total_time = total_time
        self.idx_x_true = idx_x_true
        self.idx_x_true_prop = idx_x_true_prop
        self.idx_u_true = idx_u_true
        self.idx_t = idx_t
        self.idx_y = idx_y
        self.idx_y_prop = idx_y_prop
        self.idx_s = idx_s
        self.save_compiled = save_compiled
        self.ctcs_node_intervals = ctcs_node_intervals
        self.constraints_ctcs = constraints_ctcs if constraints_ctcs is not None else []
        self.constraints_nodal = constraints_nodal if constraints_nodal is not None else []
        self.n_states = n_states
        self.n_states_prop = n_states_prop
        self.n_controls = n_controls
        self.scaling_x_overrides = scaling_x_overrides
        self.scaling_u_overrides = scaling_u_overrides
        self.__post_init__()

    def __post_init__(self):
        self.n_states = len(self.x.max)
        self.n_controls = len(self.u.max)

        def apply_overrides(size, overrides, min_arr, max_arr):
            upper = np.array(max_arr, dtype=float)
            lower = np.array(min_arr, dtype=float)
            if overrides is not None:
                for ub, lb, idx in overrides:
                    if isinstance(idx, int):
                        idxs = [idx]
                    elif isinstance(idx, slice):
                        idxs = list(range(*idx.indices(size)))
                    else:
                        idxs = list(idx)
                    ub_vals = [ub] * len(idxs) if np.isscalar(ub) else ub
                    lb_vals = [lb] * len(idxs) if np.isscalar(lb) else lb
                    for i, uval, lval in zip(idxs, ub_vals, lb_vals):
                        upper[i] = uval
                        lower[i] = lval
            return (upper, lower)
        min_x = np.array(self.x.min)
        max_x = np.array(self.x.max)
        upper_x, lower_x = apply_overrides(self.n_states, self.scaling_x_overrides, min_x, max_x)
        S_x, c_x = get_affine_scaling_matrices(self.n_states, lower_x, upper_x)
        self.S_x = S_x
        self.c_x = c_x
        self.inv_S_x = np.diag(1 / np.diag(self.S_x))
        min_u = np.array(self.u.min)
        max_u = np.array(self.u.max)
        upper_u, lower_u = apply_overrides(self.n_controls, self.scaling_u_overrides, min_u, max_u)
        S_u, c_u = get_affine_scaling_matrices(self.n_controls, lower_u, upper_u)
        self.S_u = S_u
        self.c_u = c_u
        self.inv_S_u = np.diag(1 / np.diag(self.S_u))