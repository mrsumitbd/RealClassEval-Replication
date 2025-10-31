
class Transport:

    def __init__(self):
        self.is_open = False
        self.last_request = None
        self.last_response = None

    def open(self, request):
        self.is_open = True
        self.last_request = request
        return f"Connection opened for request: {request}"

    def send(self, request):
        if not self.is_open:
            raise RuntimeError("Transport is not open. Call open() first.")
        self.last_request = request
        # Simulate sending and receiving a response
        self.last_response = f"Response to {request}"
        return self.last_response
