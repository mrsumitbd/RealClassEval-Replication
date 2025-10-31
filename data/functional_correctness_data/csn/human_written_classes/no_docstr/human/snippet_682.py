class CallbackWrapper:

    def __init__(self, callback):
        self.callback = callback

    def __call__(self, tasks):
        for task in tasks:
            self.callback(task)