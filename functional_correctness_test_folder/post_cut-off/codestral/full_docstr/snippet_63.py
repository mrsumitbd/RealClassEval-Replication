
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    total_items: int
    successful_items: int
    failed_items: int

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total_items == 0:
            return 0.0
        return (self.successful_items / self.total_items) * 100

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        return (
            f"Batch Processing Summary:\n"
            f"Total Items: {self.total_items}\n"
            f"Successful Items: {self.successful_items}\n"
            f"Failed Items: {self.failed_items}\n"
            f"Success Rate: {self.success_rate:.2f}%"
        )
