import numpy as np
from imaginaire.utils import distributed, log

class LambdaWarmUpCosineScheduler:
    """
    A learning rate scheduler that combines warm-up with a cosine decay schedule for multiple cycles.
    It supports different configurations for each cycle, including the number of warm-up steps, minimum
    and maximum scaling factors for the learning rate.

    The scheduler is intended to be used with a base learning rate of 1.0, where the actual learning
    rate at any step is the base learning rate multiplied by the scaling factor computed by the scheduler.

    Parameters:
        warm_up_steps (list[int]): List of integers where each element represents the number of warm-up
                                   steps for the corresponding cycle.
        f_min (list[float]): List of the minimum scaling factors for each cycle after warm-up.
        f_max (list[float]): List of the maximum scaling factors at the start and end of each cosine cycle.
        f_start (list[float]): List of starting scaling factors for each warm-up phase.
        cycle_lengths (list[int]): List of the total lengths of each cycle, including warm-up steps.
        verbosity_interval (int, optional): Interval of training steps at which to print current step and
                                            scaling factor information. Set to 0 by default to disable verbosity.

    Examples:
        >>> scheduler = LambdaWarmUpCosineScheduler2(
                warm_up_steps=[10, 10],
                f_min=[0.1, 0.1],
                f_max=[1.0, 1.0],
                f_start=[0.01, 0.01],
                cycle_lengths=[50, 50],
                verbosity_interval=10)
        >>> for step in range(100):
        >>>     lr_multiplier = scheduler(step)
        >>>     print(f"Step {step}: LR Multiplier = {lr_multiplier}")
    """

    def __init__(self, warm_up_steps, f_min, f_max, f_start, cycle_lengths, verbosity_interval=0):
        assert len(warm_up_steps) == len(f_min) == len(f_max) == len(f_start) == len(cycle_lengths)
        self.lr_warm_up_steps = warm_up_steps
        self.f_start = f_start
        self.f_min = f_min
        self.f_max = f_max
        self.cycle_lengths = cycle_lengths
        self.cum_cycles = np.cumsum([0] + list(self.cycle_lengths))
        self.last_f = 0.0
        self.verbosity_interval = verbosity_interval

    def find_in_interval(self, n):
        interval = 0
        for cl in self.cum_cycles[1:]:
            if n <= cl:
                return interval
            interval += 1

    def schedule(self, n, **kwargs):
        cycle = self.find_in_interval(n)
        n = n - self.cum_cycles[cycle]
        if self.verbosity_interval > 0:
            if n % self.verbosity_interval == 0:
                log.info(f'current step: {n}, recent lr-multiplier: {self.last_f}, current cycle {cycle}')
        if n < self.lr_warm_up_steps[cycle]:
            f = (self.f_max[cycle] - self.f_start[cycle]) / self.lr_warm_up_steps[cycle] * n + self.f_start[cycle]
            self.last_f = f
            return f
        else:
            t = (n - self.lr_warm_up_steps[cycle]) / (self.cycle_lengths[cycle] - self.lr_warm_up_steps[cycle])
            t = min(t, 1.0)
            f = self.f_min[cycle] + 0.5 * (self.f_max[cycle] - self.f_min[cycle]) * (1 + np.cos(t * np.pi))
            self.last_f = f
            return f

    def __call__(self, n, **kwargs):
        return self.schedule(n, **kwargs)