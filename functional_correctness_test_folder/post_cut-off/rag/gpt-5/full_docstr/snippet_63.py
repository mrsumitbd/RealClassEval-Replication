from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    succeeded: int
    failed: int
    skipped: int = 0

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        total = self.succeeded + self.failed + self.skipped
        if total <= 0:
            return 0.0
        return (self.succeeded / total) * 100.0

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        total = self.succeeded + self.failed + self.skipped
        return (
            f"Processed {total} item(s): "
            f"{self.succeeded} succeeded, {self.failed} failed, {self.skipped} skipped. "
            f"Success rate: {self.success_rate:.2f}%"
        )
