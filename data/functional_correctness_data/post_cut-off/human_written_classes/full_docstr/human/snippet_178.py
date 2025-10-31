from typing import Any
import torch
from torch_sim.state import SimState

class VelocityAutoCorrelation:
    """Calculator for velocity autocorrelation function (VACF).

    Computes VACF by averaging over atoms and dimensions, with optional
    running average across correlation windows.


    Using ``VelocityAutoCorrelation`` with
    :class:`~torch_sim.trajectory.TrajectoryReporter`::

        # Create VACF calculator
        vacf_calc = VelocityAutoCorrelation(
            window_size=100,
            device=device,
            use_running_average=True,
        )

        # Set up trajectory reporter
        reporter = TrajectoryReporter(
            "simulation_vacf.h5",
            state_frequency=100,
            prop_calculators={10: {"vacf": vacf_calc}},
        )

    """

    def __init__(self, *, window_size: int, device: torch.device, use_running_average: bool=True, normalize: bool=True) -> None:
        """Initialize VACF calculator.

        Args:
            window_size: Number of steps in correlation window
            device: Computation device
            use_running_average: Whether to compute running average across windows
            normalize: Whether to normalize correlation functions to [0,1]
        """
        self.corr_calc = CorrelationCalculator(window_size=window_size, properties={'velocity': lambda s: s.velocities}, device=device, normalize=normalize)
        self.use_running_average = use_running_average
        self._window_count = 0
        self._avg = torch.zeros(window_size, device=device)

    def __call__(self, state: SimState, _: Any=None) -> torch.Tensor:
        """Update VACF with new state.

        Args:
            state: Current simulation state
            _: Unused model argument (required property calculator interface)

        Returns:
            Tensor containing average VACF
        """
        self.corr_calc.update(state)
        if self.corr_calc.buffers['velocity'].count == self.corr_calc.window_size:
            correlations = self.corr_calc.get_auto_correlations()
            vacf = torch.mean(correlations['velocity'], dim=(1, 2))
            self._window_count += 1
            if self.use_running_average:
                factor = 1.0 / self._window_count
                self._avg += (vacf - self._avg) * factor
            else:
                self._avg = vacf
            self.corr_calc.reset()
        return torch.tensor([self._window_count], device=state.device)

    @property
    def vacf(self) -> torch.Tensor | None:
        """Current VACF result."""
        return self._avg