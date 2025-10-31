
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
        if self.context:
            self.context.report_progress(
                self.description, self.current, self.total)
