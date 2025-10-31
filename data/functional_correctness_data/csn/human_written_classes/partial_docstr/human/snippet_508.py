class WritableObject:
    """HTTP stream handler"""

    def __init__(self):
        self.content = []

    def write(self, string):
        self.content.append(string)