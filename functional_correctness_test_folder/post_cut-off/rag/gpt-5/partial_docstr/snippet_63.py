from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    total: int
    succeeded: int
    failed: int = 0
    skipped: int = 0
    duration_seconds: float | None = None

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        denom = self.total if self.total > 0 else (
            self.succeeded + self.failed + self.skipped)
        if denom <= 0:
            return 0.0
        return (self.succeeded / denom) * 100.0

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        parts = [
            f"total={self.total}",
            f"succeeded={self.succeeded}",
            f"failed={self.failed}",
            f"skipped={self.skipped}",
            f"success_rate={self.success_rate:.2f}%"
        ]
        if self.duration_seconds is not None:
            parts.append(f"duration={self.duration_seconds:.3f}s")
            if self.duration_seconds > 0:
                processed = self.succeeded + self.failed + self.skipped
                throughput = processed / self.duration_seconds
                parts.append(f"throughput={throughput:.2f}/s")
        return "BatchProcessingResult(" + ", ".join(parts) + ")"
