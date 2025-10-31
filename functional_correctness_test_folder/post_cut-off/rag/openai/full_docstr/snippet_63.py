
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    total: int
    successes: int
    failures: int

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total == 0:
            return 0.0
        return (self.successes / self.total) * 100.0

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        return (
            f"Processed {self.total} items: "
            f"{self.successes} succeeded, {self.failures} failed. "
            f"Success rate: {self.success_rate:.2f}%"
        )
