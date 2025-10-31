
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    total: int
    successful: int
    failed: int

    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.successful / self.total

    def summary(self) -> str:
        return (f"Total: {self.total}, Successful: {self.successful}, "
                f"Failed: {self.failed}, Success Rate: {self.success_rate:.2%}")
