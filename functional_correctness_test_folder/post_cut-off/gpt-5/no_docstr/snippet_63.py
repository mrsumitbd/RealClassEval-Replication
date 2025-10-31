from dataclasses import dataclass
from typing import Optional


@dataclass
class BatchProcessingResult:
    succeeded: int = 0
    failed: int = 0
    skipped: int = 0
    duration_seconds: Optional[float] = None

    @property
    def success_rate(self) -> float:
        denominator = self.succeeded + self.failed
        if denominator <= 0:
            return 0.0
        return self.succeeded / denominator

    def summary(self) -> str:
        total = self.succeeded + self.failed + self.skipped
        rate_percent = self.success_rate * 100
        duration_part = (
            f", duration={self.duration_seconds:.3f}s" if self.duration_seconds is not None else ""
        )
        return (
            f"Processed {total} items: "
            f"succeeded={self.succeeded}, failed={self.failed}, skipped={self.skipped}, "
            f"success_rate={rate_percent:.2f}%{duration_part}"
        )
