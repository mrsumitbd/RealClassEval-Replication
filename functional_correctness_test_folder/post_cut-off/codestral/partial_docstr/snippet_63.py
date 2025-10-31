
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    total_items: int
    successful_items: int

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total_items == 0:
            return 0.0
        return (self.successful_items / self.total_items) * 100

    def summary(self) -> str:
        return f"Processed {self.total_items} items with {self.successful_items} successful and {self.total_items - self.successful_items} failed. Success rate: {self.success_rate:.2f}%"
