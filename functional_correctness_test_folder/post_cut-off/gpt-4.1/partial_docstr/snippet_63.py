
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    total: int
    success: int
    failure: int

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total == 0:
            return 0.0
        return (self.success / self.total) * 100

    def summary(self) -> str:
        return (f"Total: {self.total}, Success: {self.success}, "
                f"Failure: {self.failure}, Success Rate: {self.success_rate:.2f}%")
