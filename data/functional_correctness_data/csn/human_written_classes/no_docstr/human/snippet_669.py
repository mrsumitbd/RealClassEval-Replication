class StdoutFilter:

    def __init__(self, parent):
        self.parent = parent

    def write(self, data):
        message = data
        self.parent.write(message, True)

    def flush(self):
        pass