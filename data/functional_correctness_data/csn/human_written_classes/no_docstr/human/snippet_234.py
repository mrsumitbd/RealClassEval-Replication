class ErrorReporter:

    def __init__(self, reporters):
        self.targets = [target for target in reporters]

    def report(self):
        for t in self.targets:
            t.report()