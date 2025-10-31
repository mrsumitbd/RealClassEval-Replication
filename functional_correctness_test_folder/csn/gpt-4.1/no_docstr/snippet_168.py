
class Gateway:

    def __init__(self, req):
        self.req = req

    def respond(self):
        if isinstance(self.req, dict):
            return {"status": "success", "data": self.req}
        elif isinstance(self.req, str):
            return {"status": "success", "message": self.req}
        elif self.req is None:
            return {"status": "error", "message": "No request provided"}
        else:
            return {"status": "error", "message": "Invalid request type"}
