
from dataclasses import dataclass, field
from typing import List


@dataclass
class BatchProcessingResult:
    total_tasks: int = field(default=0)
    successful_tasks: int = field(default=0)

    @property
    def success_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return self.successful_tasks / self.total_tasks

    def summary(self) -> str:
        return (f"Total tasks: {self.total_tasks}, "
                f"Successful tasks: {self.successful_tasks}, "
                f"Success rate: {self.success_rate:.2%}")
