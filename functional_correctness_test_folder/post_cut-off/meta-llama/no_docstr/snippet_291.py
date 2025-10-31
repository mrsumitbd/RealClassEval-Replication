
class ProgressScope:

    def __init__(self, context: 'MCPContext', total: int, description: str):
        self.context = context
        self.total = total
        self.description = description
        self.current = 0

    def update(self, step: int = 1) -> None:
        self.set_progress(self.current + step)

    def set_progress(self, current: int) -> None:
        if current < 0 or current > self.total:
            raise ValueError("Current progress is out of range")
        self.current = current
        # Assuming MCPContext has a method to update progress
        self.context.update_progress(
            self.description, self.current, self.total)
