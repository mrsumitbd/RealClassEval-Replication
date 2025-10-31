
from dataclasses import dataclass, field
from typing import List


@dataclass
class BatchProcessingResult:
    successes: int = 0
    failures: int = 0
    total_items: int = field(init=False)

    def __post_init__(self):
        self.total_items = self.successes + self.failures

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total_items == 0:
            return 0.0
        return (self.successes / self.total_items) * 100

    def summary(self) -> str:
        return f"Processed {self.total_items} items. Success rate: {self.success_rate:.2f}% ({self.successes} successes, {self.failures} failures)"
