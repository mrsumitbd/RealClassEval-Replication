
from dataclasses import dataclass, field


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    total: int = field(default=0)
    succeeded: int = field(default=0)
    failed: int = field(default=0)

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total == 0:
            return 0.0
        return (self.succeeded / self.total) * 100

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        return (f"Batch Processing Summary:\n"
                f"Total: {self.total}\n"
                f"Succeeded: {self.succeeded}\n"
                f"Failed: {self.failed}\n"
                f"Success Rate: {self.success_rate:.2f}%")
