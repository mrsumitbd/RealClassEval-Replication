class Gateway:
    '''Base class to interface HTTPServer with other systems, such as WSGI.'''

    def __init__(self, req):
        # Store the incoming request object
        self.req = req
        # Default response components
        self.status = 200
        self.headers = {'Content-Type': 'text/plain'}
        self.body = b''

    def respond(self):
        """
        Return a tuple suitable for an HTTP response:
        (status_code, headers_dict, body_bytes)
        """
        return self.status, self.headers, self.body

    # Optional helper to set a custom response
    def set_response(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body if isinstance(body, (bytes, bytearray)) else body.encode(
            'utf-8') if isinstance(body, str) else str(body).encode('utf-8')
