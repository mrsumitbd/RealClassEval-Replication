class Gateway:
    def __init__(self, req):
        self.req = req

    def respond(self):
        return {
            "status": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {"received": self.req}
        }
