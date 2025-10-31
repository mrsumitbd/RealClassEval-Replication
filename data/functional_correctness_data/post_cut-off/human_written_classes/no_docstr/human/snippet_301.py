class RaySimpleMock:

    def __init__(self):
        self.remote = RemoteDecorator()

    def get(self, value):
        return value