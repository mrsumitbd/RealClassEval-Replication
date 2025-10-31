from dataclasses import dataclass

@dataclass()
class _ErrorSummary:
    """Contains data for errors of a node."""
    origin: str
    example_message: str
    failed_indexed_executions: list[tuple[int, str]]

    def add_execution(self, index: int, name: str) -> None:
        """Adds an execution to the summary."""
        self.failed_indexed_executions.append((index, name))

    @property
    def num_failed(self) -> int:
        """Helps with jinja"""
        return len(self.failed_indexed_executions)