
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    successful: int
    failed: int
    total: int

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        return (self.successful / self.total) * 100 if self.total > 0 else 0.0

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        return f"Successful: {self.successful}, Failed: {self.failed}, Total: {self.total}, Success Rate: {self.success_rate:.2f}%"
