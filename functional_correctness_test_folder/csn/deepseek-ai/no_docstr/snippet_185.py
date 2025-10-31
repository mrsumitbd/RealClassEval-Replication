
class Transport:

    def __init__(self):
        self.is_open = False

    def open(self, request):
        self.is_open = True
        return f"Opened with request: {request}"

    def send(self, request):
        if not self.is_open:
            raise Exception("Transport is not open")
        return f"Sent request: {request}"
