
from dataclasses import dataclass, field
from typing import List


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    total_tasks: int
    successful_tasks: int

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        return (self.successful_tasks / self.total_tasks) * 100 if self.total_tasks > 0 else 0.0

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        return (f"Total tasks: {self.total_tasks}, "
                f"Successful tasks: {self.successful_tasks}, "
                f"Success rate: {self.success_rate:.2f}%")
