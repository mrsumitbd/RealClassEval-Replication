from typing import Callable, Optional
from dataclasses import dataclass

@dataclass
class ScpConfig:

    def __init__(self, n: Optional[int]=None, k_max: int=200, w_tr: float=1.0, lam_vc: float=1.0, ep_tr: float=0.0001, ep_vb: float=0.0001, ep_vc: float=1e-08, lam_cost: float=0.0, lam_vb: float=0.0, uniform_time_grid: bool=False, cost_drop: int=-1, cost_relax: float=1.0, w_tr_adapt: float=1.0, w_tr_max: Optional[float]=None, w_tr_max_scaling_factor: Optional[float]=None):
        """
        Configuration class for Sequential Convex Programming (SCP).

        This class defines the parameters used to configure the SCP solver. You
        will very likely need to modify the weights for your problem. Please
        refer to my guide [here](https://haynec.github.io/openscvx/
        hyperparameter_tuning) for more information.

        Attributes:
            n (int): The number of discretization nodes. Defaults to `None`.
            k_max (int): The maximum number of SCP iterations. Defaults to 200.
            w_tr (float): The trust region weight. Defaults to 1.0.
            lam_vc (float): The penalty weight for virtual control. Defaults to 1.0.
            ep_tr (float): The trust region convergence tolerance. Defaults to 1e-4.
            ep_vb (float): The boundary constraint convergence tolerance.
                Defaults to 1e-4.
            ep_vc (float): The virtual constraint convergence tolerance.
                Defaults to 1e-8.
            lam_cost (float): The weight for original cost. Defaults to 0.0.
            lam_vb (float): The weight for virtual buffer. This is only used if
                there are nonconvex nodal constraints present. Defaults to 0.0.
            uniform_time_grid (bool): Whether to use a uniform time grid.
                Defaults to `False`.
            cost_drop (int): The number of iterations to allow for cost
                stagnation before termination. Defaults to -1 (disabled).
            cost_relax (float): The relaxation factor for cost reduction.
                Defaults to 1.0.
            w_tr_adapt (float): The adaptation factor for the trust region
                weight. Defaults to 1.0.
            w_tr_max (float): The maximum allowable trust region weight.
                Defaults to `None`.
            w_tr_max_scaling_factor (float): The scaling factor for the maximum
                trust region weight. Defaults to `None`.
        """
        self.n = n
        self.k_max = k_max
        self.w_tr = w_tr
        self.lam_vc = lam_vc
        self.ep_tr = ep_tr
        self.ep_vb = ep_vb
        self.ep_vc = ep_vc
        self.lam_cost = lam_cost
        self.lam_vb = lam_vb
        self.uniform_time_grid = uniform_time_grid
        self.cost_drop = cost_drop
        self.cost_relax = cost_relax
        self.w_tr_adapt = w_tr_adapt
        self.w_tr_max = w_tr_max
        self.w_tr_max_scaling_factor = w_tr_max_scaling_factor

    def __post_init__(self):
        keys_to_scale = ['w_tr', 'lam_vc', 'lam_cost', 'lam_vb']
        scale = max((getattr(self, key) for key in keys_to_scale))
        for key in keys_to_scale:
            setattr(self, key, getattr(self, key) / scale)
        if self.w_tr_max_scaling_factor is not None and self.w_tr_max is None:
            self.w_tr_max = self.w_tr_max_scaling_factor * self.w_tr