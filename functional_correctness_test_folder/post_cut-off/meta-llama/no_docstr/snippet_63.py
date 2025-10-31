
from dataclasses import dataclass, field
from typing import List


@dataclass
class BatchProcessingResult:
    successes: int = 0
    failures: int = 0
    total_items: int = field(init=False)
    error_messages: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.total_items = self.successes + self.failures

    @property
    def success_rate(self) -> float:
        if self.total_items == 0:
            return 0.0
        return self.successes / self.total_items

    def summary(self) -> str:
        summary_str = f"Processed {self.total_items} items. Success rate: {self.success_rate * 100:.2f}%"
        if self.failures > 0:
            summary_str += f"\nFailed items: {self.failures}"
            for i, error in enumerate(self.error_messages, start=1):
                summary_str += f"\n{i}. {error}"
        return summary_str
