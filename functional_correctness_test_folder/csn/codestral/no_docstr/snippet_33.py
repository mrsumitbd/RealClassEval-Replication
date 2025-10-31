
class ExceptionHandler:

    def wants(self, exc):
        return isinstance(exc, Exception)

    def handle(self, exc):
        print(f"An exception occurred: {exc}")
