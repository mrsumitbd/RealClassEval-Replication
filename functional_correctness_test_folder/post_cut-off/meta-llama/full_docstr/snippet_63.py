
from dataclasses import dataclass, field
from typing import List


@dataclass
class BatchProcessingResult:
    '''Result of batch processing operation'''
    total_items: int = 0
    successful_items: int = 0
    failed_items: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        '''Calculate success rate as percentage'''
        if self.total_items == 0:
            return 0.0
        return (self.successful_items / self.total_items) * 100

    def summary(self) -> str:
        '''Generate a summary of the batch processing results'''
        summary_str = f"Total items: {self.total_items}\n"
        summary_str += f"Successful items: {self.successful_items}\n"
        summary_str += f"Failed items: {len(self.failed_items)}\n"
        summary_str += f"Success rate: {self.success_rate:.2f}%\n"
        if self.failed_items:
            summary_str += "Failed item details:\n"
            for item in self.failed_items:
                summary_str += f"- {item}\n"
        return summary_str.strip()

# Example usage:


def main():
    result = BatchProcessingResult()
    result.total_items = 10
    result.successful_items = 8
    result.failed_items = ["item1", "item2"]
    print(result.summary())


if __name__ == "__main__":
    main()
