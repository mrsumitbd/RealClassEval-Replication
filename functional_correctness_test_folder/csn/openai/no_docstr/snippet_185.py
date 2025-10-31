
import urllib.request
import urllib.error


class Transport:
    def __init__(self):
        self._request = None
        self._response = None

    def open(self, request):
        """
        Prepare a request for sending.

        Parameters
        ----------
        request : dict
            Dictionary containing request details. Expected keys:
            - 'method': HTTP method (default 'GET')
            - 'url': Target URL (required)
            - 'headers': Dictionary of HTTP headers (optional)
            - 'body': Request body as str or bytes (optional)
        """
        if not isinstance(request, dict):
            raise TypeError("request must be a dict")

        method = request.get("method", "GET").upper()
        url = request.get("url")
        if not url:
            raise ValueError("request must contain a 'url' key")

        headers = request.get("headers", {})
        if not isinstance(headers, dict):
            raise TypeError("'headers' must be a dict")

        body = request.get("body")
        if body is not None:
            if isinstance(body, str):
                body = body.encode("utf-8")
            elif not isinstance(body, (bytes, bytearray)):
                raise TypeError("'body' must be str, bytes, or bytearray")

        self._request = urllib.request.Request(
            url=url,
            data=body,
            headers=headers,
            method=method,
        )

    def send(self, request=None):
        """
        Send the prepared request and return the response body.

        Parameters
        ----------
        request : dict, optional
            If provided, the request will be opened before sending.

        Returns
        -------
        bytes
            The raw response body.
        """
        if request is not None:
            self.open(request)

        if self._request is None:
            raise RuntimeError("No request has been opened")

        try:
            with urllib.request.urlopen(self._request) as resp:
                self._response = resp.read()
        except urllib.error.HTTPError as e:
            # Return the error body if available
            self._response = e.read()
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to send request: {e}") from e

        return self._response
