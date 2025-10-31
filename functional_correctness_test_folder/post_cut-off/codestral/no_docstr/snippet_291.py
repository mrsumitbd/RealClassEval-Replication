
class ProgressScope:

    def __init__(self, context: 'MCPContext', total: int, description: str):
        self.context = context
        self.total = total
        self.description = description
        self.current = 0

    def update(self, step: int = 1) -> None:
        self.current += step
        self.context.update_progress(
            self.current, self.total, self.description)

    def set_progress(self, current: int) -> None:
        self.current = current
        self.context.update_progress(
            self.current, self.total, self.description)
