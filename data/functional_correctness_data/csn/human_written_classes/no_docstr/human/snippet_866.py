class EventHolder:

    def __init__(self, event, path, condition_manager):
        self.event = event
        self.path = path
        self.condition_manager = condition_manager
        self.failed = False

    def release(self):
        self.event.set()

    def fail(self):
        self.failed = True