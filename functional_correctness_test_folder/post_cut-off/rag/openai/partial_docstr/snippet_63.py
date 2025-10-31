
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    total_items: int
    successful_items: int
    failed_items: int
    errors: Optional[List[str]] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total_items == 0:
            return 0.0
        return (self.successful_items / self.total_items) * 100.0

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        parts = [
            f"Processed {self.total_items} items:",
            f"{self.successful_items} succeeded",
            f"{self.failed_items} failed",
        ]
        if self.errors:
            parts.append(f"Errors: {', '.join(self.errors)}")
        return "; ".join(parts)
