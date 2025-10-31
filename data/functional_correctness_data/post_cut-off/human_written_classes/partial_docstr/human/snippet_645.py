from pydantic.dataclasses import dataclass
import copy

@dataclass
class Particle:
    steps: list[str]
    is_stopped: bool
    partial_log_weights: list[float]

    @property
    def log_weight(self) -> float:
        """Return the most recent log weight."""
        if self.partial_log_weights:
            return self.partial_log_weights[-1]
        return 0.0

    def deepcopy(self):
        return Particle(steps=copy.deepcopy(self.steps), is_stopped=self.is_stopped, partial_log_weights=copy.deepcopy(self.partial_log_weights))