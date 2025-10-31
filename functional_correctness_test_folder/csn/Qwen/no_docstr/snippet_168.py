
class Gateway:

    def __init__(self, req):
        self.req = req

    def respond(self):
        # Assuming a simple echo response for demonstration
        return f"Received request: {self.req}"
