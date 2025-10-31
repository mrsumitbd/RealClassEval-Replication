class NOOPStatus:

    def __init__(self, message: str, **kwargs):
        self.message = message

    def __enter__(self):
        print(self.message)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass