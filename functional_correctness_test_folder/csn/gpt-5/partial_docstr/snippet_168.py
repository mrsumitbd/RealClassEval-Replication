class Gateway:
    '''Base class to interface HTTPServer with other systems, such as WSGI.'''

    def __init__(self, req):
        if req is None:
            raise ValueError("req must not be None")
        self.req = req

    def respond(self):
        raise NotImplementedError("Subclasses must implement respond()")
