from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    succeeded: int = 0
    failed: int = 0
    skipped: int = 0

    @property
    def total(self) -> int:
        return self.succeeded + self.failed + self.skipped

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        total = self.total
        return (self.succeeded / total * 100.0) if total else 0.0

    def summary(self) -> str:
        return (
            f"{self.succeeded} succeeded, {self.failed} failed, {self.skipped} skipped "
            f"out of {self.total} items ({self.success_rate:.2f}% success)"
        )
