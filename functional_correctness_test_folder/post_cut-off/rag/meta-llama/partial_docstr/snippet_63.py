
from dataclasses import dataclass
from typing import List


@dataclass
class BatchProcessingResult:
    """Result of batch processing operation"""
    processed_count: int
    success_count: int
    failed_count: int
    errors: List[str]

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage"""
        if self.processed_count == 0:
            return 0.0
        return (self.success_count / self.processed_count) * 100

    def summary(self) -> str:
        """Generate a summary of the batch processing results"""
        summary_str = f"Processed: {self.processed_count}, Success: {self.success_count}, Failed: {self.failed_count}\n"
        summary_str += f"Success Rate: {self.success_rate:.2f}%\n"
        if self.errors:
            summary_str += "Errors:\n"
            for error in self.errors:
                summary_str += f"- {error}\n"
        return summary_str
