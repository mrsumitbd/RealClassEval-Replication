
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    successes: int
    total: int

    @property
    def success_rate(self) -> float:
        """Return the success rate as a float between 0 and 1."""
        if self.total == 0:
            return 0.0
        return self.successes / self.total

    def summary(self) -> str:
        """Return a human‑readable summary of the batch processing result."""
        rate = self.success_rate
        return (
            f"Processed {self.total} items: "
            f"{self.successes} succeeded, "
            f"{self.total - self.successes} failed. "
            f"Success rate: {rate:.2%}"
        )
