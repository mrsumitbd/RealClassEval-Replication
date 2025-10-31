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
        processed = self.succeeded + self.failed
        if processed == 0:
            return 0.0
        return (self.succeeded / processed) * 100.0

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        total = self.succeeded + self.failed + self.skipped
        processed = self.succeeded + self.failed
        return (
            f"Batch processing results: total={total}, "
            f"processed={processed}, succeeded={self.succeeded}, "
            f"failed={self.failed}, skipped={self.skipped}, "
            f"success_rate={self.success_rate:.2f}%"
        )
