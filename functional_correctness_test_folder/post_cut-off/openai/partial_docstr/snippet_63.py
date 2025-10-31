
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    successes: int = 0
    total: int = 0

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total == 0:
            return 0.0
        return (self.successes / self.total) * 100

    def summary(self) -> str:
        """Return a human‑readable summary of the batch processing results."""
        rate = self.success_rate
        return (
            f"Processed {self.total} items: "
            f"{self.successes} succeeded, "
            f"{self.total - self.successes} failed "
            f"({rate:.2f}% success rate)."
        )
