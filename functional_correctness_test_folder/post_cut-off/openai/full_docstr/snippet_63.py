
from dataclasses import dataclass, field


@dataclass
class BatchProcessingResult:
    total_items: int
    successful_items: int
    failed_items: int | None = None

    def __post_init__(self):
        if self.failed_items is None:
            self.failed_items = self.total_items - self.successful_items
        if self.failed_items < 0:
            raise ValueError("failed_items cannot be negative")

    @property
    def success_rate(self) -> float:
        if self.total_items == 0:
            return 0.0
        return (self.successful_items / self.total_items) * 100

    def summary(self) -> str:
        return (
            f"Processed {self.total_items} items: "
            f"{self.successful_items} succeeded, "
            f"{self.failed_items} failed. "
            f"Success rate: {self.success_rate:.2f}%"
        )
