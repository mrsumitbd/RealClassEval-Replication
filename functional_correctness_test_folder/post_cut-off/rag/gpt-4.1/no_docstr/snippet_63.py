from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    total: int
    succeeded: int
    failed: int
    errors: List[str]

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total == 0:
            return 0.0
        return (self.succeeded / self.total) * 100.0

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        summary_lines = [
            f"Batch Processing Summary:",
            f"  Total: {self.total}",
            f"  Succeeded: {self.succeeded}",
            f"  Failed: {self.failed}",
            f"  Success Rate: {self.success_rate:.2f}%",
        ]
        if self.failed > 0 and self.errors:
            summary_lines.append("  Errors:")
            for err in self.errors:
                summary_lines.append(f"    - {err}")
        return "\n".join(summary_lines)
