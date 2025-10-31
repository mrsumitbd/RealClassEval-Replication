from dataclasses import dataclass, field


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    successes: int = 0
    failures: int = 0
    errors: int = 0
    skipped: int = 0
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        for name in ("successes", "failures", "errors", "skipped"):
            value = getattr(self, name)
            if not isinstance(value, int):
                raise TypeError(f"{name} must be an int")
            if value < 0:
                raise ValueError(f"{name} cannot be negative")

    @property
    def attempted(self) -> int:
        return self.successes + self.failures + self.errors

    @property
    def total(self) -> int:
        return self.attempted + self.skipped

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        denom = self.attempted
        if denom == 0:
            return 0.0
        return (self.successes / denom) * 100.0

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        return (
            f"Batch Processing Summary: "
            f"total={self.total}, attempted={self.attempted}, "
            f"successes={self.successes}, failures={self.failures}, errors={self.errors}, skipped={self.skipped}, "
            f"success_rate={self.success_rate:.2f}%"
        )
