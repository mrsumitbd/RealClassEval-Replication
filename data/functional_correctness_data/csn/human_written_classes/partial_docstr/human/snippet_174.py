from typing import Union, Any, Tuple, List, Callable, Optional, Dict
import numpy as np

class StepSizer:
    """
    This class abstracts complicated step size logic out of the fitters. The API is as follows:

    > step_sizer = StepSizer(initial_step_size)
    > step_size = step_sizer.next()
    > step_sizer.update(some_convergence_norm)
    > step_size = step_sizer.next()


    ATM it contains lots of "magic constants"
    """

    def __init__(self, initial_step_size: float):
        self.initial_step_size = initial_step_size
        self.step_size = initial_step_size
        self.temper_back_up = False
        self.norm_of_deltas: List[float] = []

    def update(self, norm_of_delta: float) -> 'StepSizer':
        SCALE = 1.3
        LOOKBACK = 3
        self.norm_of_deltas.append(norm_of_delta)
        if self.temper_back_up:
            self.step_size = min(self.step_size * SCALE, self.initial_step_size)
        if norm_of_delta >= 15.0:
            self.step_size *= 0.1
            self.temper_back_up = True
        elif 15.0 > norm_of_delta > 5.0:
            self.step_size *= 0.25
            self.temper_back_up = True
        if len(self.norm_of_deltas) >= LOOKBACK and (not self._is_monotonically_decreasing(self.norm_of_deltas[-LOOKBACK:])):
            self.step_size *= 0.98
        if len(self.norm_of_deltas) >= LOOKBACK and self._is_monotonically_decreasing(self.norm_of_deltas[-LOOKBACK:]):
            self.step_size = min(self.step_size * SCALE, 1.0)
        return self

    @staticmethod
    def _is_monotonically_decreasing(array: Union[List[float], List[float]]) -> bool:
        return np.all(np.diff(array) < 0)

    def next(self) -> float:
        return self.step_size