
class ProgressScope:

    def __init__(self, context: 'MCPContext', total: int, description: str):
        self.context = context
        self.total = total
        self.description = description
        self.current = 0

    def update(self, step: int = 1) -> None:
        self.current += step
        self._report_progress()

    def set_progress(self, current: int) -> None:
        self.current = current
        self._report_progress()

    def _report_progress(self) -> None:
        if self.total > 0:
            progress = (self.current / self.total) * 100
            print(f"{self.description}: {progress:.2f}%")
        else:
            print(f"{self.description}: {self.current} steps completed")
