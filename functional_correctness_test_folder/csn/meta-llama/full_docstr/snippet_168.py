
class Gateway:
    '''Base class to interface HTTPServer with other systems, such as WSGI.'''

    def __init__(self, req):
        '''Initialize Gateway instance with request.
        Args:
            req (HTTPRequest): current HTTP request
        '''
        self.req = req

    def respond(self):
        '''Process the current request. Must be overridden in a subclass.'''
        raise NotImplementedError("Subclasses must implement respond method")
