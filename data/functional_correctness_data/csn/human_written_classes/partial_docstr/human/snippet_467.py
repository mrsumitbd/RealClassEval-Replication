class dummy:
    """
    Instances of this class can be used as an attribute container.
    """

    def __init__(self):
        self.token = None

    def set(self, value):
        self.token = value

    def get(self):
        return self.token