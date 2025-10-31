
from dataclasses import dataclass
from typing import Any


@dataclass
class BatchProcessingResult:
    """Result of batch processing operation"""
    total: int
    success: int
    failed: int

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage"""
        if self.total == 0:
            return 0.0
        return (self.success / self.total) * 100

    def summary(self) -> str:
        """Generate a summary of the batch processing results"""
        return f"Total: {self.total}, Success: {self.success}, Failed: {self.failed}, Success Rate: {self.success_rate:.2f}%"
