
class Gateway:
    '''Base class to interface HTTPServer with other systems, such as WSGI.'''

    def __init__(self, req):
        """
        Initialize the Gateway instance.

        :param req: The HTTP request object.
        """
        self.req = req
        self.response_status = None
        self.response_headers = []
        self.response_body = None

    def respond(self):
        """
        Generate a response based on the request.

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement respond()")
