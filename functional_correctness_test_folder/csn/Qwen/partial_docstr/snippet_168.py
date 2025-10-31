
class Gateway:
    '''Base class to interface HTTPServer with other systems, such as WSGI.'''

    def __init__(self, req):
        self.req = req

    def respond(self):
        raise NotImplementedError(
            "This method should be overridden by subclasses.")
