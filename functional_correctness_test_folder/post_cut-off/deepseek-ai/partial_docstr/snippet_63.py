
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    total: int
    successful: int

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total == 0:
            return 0.0
        return (self.successful / self.total) * 100.0

    def summary(self) -> str:
        return f"Total: {self.total}, Successful: {self.successful}, Success Rate: {self.success_rate:.2f}%"
