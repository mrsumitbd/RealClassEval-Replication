
from dataclasses import dataclass


@dataclass
class BatchProcessingResult:
    total_tasks: int
    successful_tasks: int

    @property
    def success_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return self.successful_tasks / self.total_tasks

    def summary(self) -> str:
        return f"Batch Processing Summary: {self.successful_tasks} successful out of {self.total_tasks} tasks (Success Rate: {self.success_rate:.2%})"
