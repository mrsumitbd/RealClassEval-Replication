
class Transport:

    def __init__(self):
        self.connection = None

    def open(self, request):
        # Simulate opening a connection
        self.connection = f"Connection opened with request: {request}"
        return self.connection

    def send(self, request):
        # Simulate sending a request
        if self.connection:
            return f"Sent request: {request} over {self.connection}"
        else:
            return "No connection open. Please open a connection first."
