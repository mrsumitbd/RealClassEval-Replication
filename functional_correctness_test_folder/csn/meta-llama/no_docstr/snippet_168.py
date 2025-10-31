
class Gateway:

    def __init__(self, req):
        """
        Initialize the Gateway class.

        Args:
            req (Request): The incoming request object.
        """
        self.req = req
        self.response = None

    def respond(self):
        """
        Process the incoming request and generate a response.

        Returns:
            Response: The response object.
        """
        # Assuming req has method and path attributes
        if self.req.method == 'GET':
            # Handle GET request
            self.response = self._handle_get(self.req.path)
        elif self.req.method == 'POST':
            # Handle POST request
            self.response = self._handle_post(self.req.path, self.req.data)
        else:
            # Handle unsupported methods
            self.response = self._handle_error(405, 'Method Not Allowed')

        return self.response

    def _handle_get(self, path):
        # Implement GET request handling logic here
        # For demonstration purposes, assume a simple response
        return Response(200, 'OK', {'Content-Type': 'text/plain'}, f'GET request received for {path}')

    def _handle_post(self, path, data):
        # Implement POST request handling logic here
        # For demonstration purposes, assume a simple response
        return Response(201, 'Created', {'Content-Type': 'text/plain'}, f'POST request received for {path} with data: {data}')

    def _handle_error(self, status_code, message):
        # Implement error handling logic here
        # For demonstration purposes, assume a simple error response
        return Response(status_code, message, {'Content-Type': 'text/plain'}, message)


class Request:
    def __init__(self, method, path, data=None):
        self.method = method
        self.path = path
        self.data = data


class Response:
    def __init__(self, status_code, status_message, headers, body):
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers
        self.body = body

    def __repr__(self):
        return f'Response(status_code={self.status_code}, status_message={self.status_message}, headers={self.headers}, body={self.body})'


# Example usage
if __name__ == '__main__':
    req = Request('GET', '/example')
    gateway = Gateway(req)
    response = gateway.respond()
    print(response)

    req_post = Request('POST', '/example', 'Hello, World!')
    gateway_post = Gateway(req_post)
    response_post = gateway_post.respond()
    print(response_post)
