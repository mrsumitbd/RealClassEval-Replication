
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    total_items: int
    successful_items: int

    @property
    def success_rate(self) -> float:
        if self.total_items == 0:
            return 0.0
        return self.successful_items / self.total_items

    def summary(self) -> str:
        return f"Processed {self.total_items} items with {self.successful_items} successes ({self.success_rate:.2%} success rate)"
