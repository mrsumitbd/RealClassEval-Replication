
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BatchProcessingResult:
    """Result of batch processing operation"""

    total_items: int
    successful_items: int
    failed_items: int
    errors: Optional[List[str]] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage"""
        if self.total_items == 0:
            return 0.0
        return (self.successful_items / self.total_items) * 100.0

    def summary(self) -> str:
        """Generate a summary of the batch processing results"""
        lines = [
            f"Total items processed: {self.total_items}",
            f"Successful items: {self.successful_items}",
            f"Failed items: {self.failed_items}",
            f"Success rate: {self.success_rate:.2f}%",
        ]
        if self.errors:
            lines.append(f"Errors ({len(self.errors)}):")
            lines.extend(f"  - {e}" for e in self.errors)
        return "\n".join(lines)
