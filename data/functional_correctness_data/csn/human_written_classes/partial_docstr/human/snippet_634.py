import httpx

class Response:
    """Handles the Planet server's response to a HTTP request."""

    def __init__(self, http_response: httpx.Response):
        """Initialize object.

        Parameters:
            http_response: Response that was received from the server.
        """
        self._http_response = http_response

    def __repr__(self):
        return f'<models.Response [{self.status_code}]>'

    @property
    def status_code(self) -> int:
        """HTTP status code"""
        return self._http_response.status_code

    def json(self) -> dict:
        """Response json"""
        return self._http_response.json()