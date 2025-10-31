
from dataclasses import dataclass, field
from typing import List


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    total_tasks: int
    successful_tasks: int
    failed_tasks: int

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total_tasks == 0:
            return 0.0
        return (self.successful_tasks / self.total_tasks) * 100

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        return (f"Total tasks: {self.total_tasks}\n"
                f"Successful tasks: {self.successful_tasks}\n"
                f"Failed tasks: {self.failed_tasks}\n"
                f"Success rate: {self.success_rate:.2f}%")
