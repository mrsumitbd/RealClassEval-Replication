
class ProgressScope:

    def __init__(self, context: 'MCPContext', total: int, description: str):
        self.context = context
        self.total = total
        self.description = description
        self.current = 0

    def update(self, step: int = 1) -> None:
        self.current += step
        if self.current > self.total:
            self.current = self.total

    def set_progress(self, current: int) -> None:
        if current < 0:
            current = 0
        elif current > self.total:
            current = self.total
        self.current = current
