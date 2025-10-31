class FakeFuture:

    def __init__(self, task, executor):
        self.task = task
        self.executor = executor

    def result(self):
        return self.executor.loop.run_until_complete(self.task)