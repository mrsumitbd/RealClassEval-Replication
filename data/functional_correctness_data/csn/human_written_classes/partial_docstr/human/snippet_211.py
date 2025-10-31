import numpy as np

class Metric:
    """Represents the history of a single metric."""

    def __init__(self, history, name):
        self.name = name
        self.steps = history.steps
        self.data = np.array([history.history[s].get(name) for s in self.steps])

    @property
    def formatted_steps(self):
        return [format_step(s) for s in self.steps]