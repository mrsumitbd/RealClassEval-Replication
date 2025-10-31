
from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict
import numpy as np


@dataclass
class OptimizationResults:
    converged: bool
    t_final: float
    u: Any  # Control type (placeholder)
    x: Any  # State type (placeholder)
    x_history: List[np.ndarray] = field(default_factory=list)
    u_history: List[np.ndarray] = field(default_factory=list)
    discretization_history: List[np.ndarray] = field(default_factory=list)
    J_tr_history: List[np.ndarray] = field(default_factory=list)
    J_vb_history: List[np.ndarray] = field(default_factory=list)
    J_vc_history: List[np.ndarray] = field(default_factory=list)
    t_full: Optional[np.ndarray] = None
    x_full: Optional[np.ndarray] = None
    u_full: Optional[np.ndarray] = None
    cost: Optional[float] = None
    ctcs_violation: Optional[np.ndarray] = None
    plotting_data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        pass

    def update_plotting_data(self, **kwargs):
        self.plotting_data.update(kwargs)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            return self.plotting_data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            if key in self.plotting_data:
                return self.plotting_data[key]
            raise KeyError(f"Key '{key}' not found in results")

    def __setitem__(self, key: str, value: Any):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.plotting_data[key] = value

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key) or key in self.plotting_data

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'converged': self.converged,
            't_final': self.t_final,
            'u': self.u,
            'x': self.x,
            'x_history': self.x_history,
            'u_history': self.u_history,
            'discretization_history': self.discretization_history,
            'J_tr_history': self.J_tr_history,
            'J_vb_history': self.J_vb_history,
            'J_vc_history': self.J_vc_history,
            't_full': self.t_full,
            'x_full': self.x_full,
            'u_full': self.u_full,
            'cost': self.cost,
            'ctcs_violation': self.ctcs_violation,
        }
        result.update(self.plotting_data)
        return result
