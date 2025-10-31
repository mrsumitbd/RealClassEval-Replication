
class Gateway:
    '''Base class to interface HTTPServer with other systems, such as WSGI.'''

    def __init__(self, req):
        self.req = req

    def respond(self):
        # This base class does nothing; subclasses should override this method.
        pass
