
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    total: int
    successful: int
    failed: int

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total == 0:
            return 0.0
        return (self.successful / self.total) * 100

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        return f"Total: {self.total}, Successful: {self.successful}, Failed: {self.failed}, Success Rate: {self.success_rate:.2f}%"
