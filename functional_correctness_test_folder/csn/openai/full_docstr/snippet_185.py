
import urllib.request
import urllib.error
import http.cookiejar
from typing import Dict, Any, Optional, Union


class TransportError(Exception):
    """Raised for all transport related errors."""
    pass


class Request:
    """
    Simple transport request representation.
    """

    def __init__(
        self,
        url: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Union[str, bytes]] = None,
        proxies: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
    ):
        self.url = url
        self.method = method.upper()
        self.headers = headers or {}
        self.body = body
        self.proxies = proxies or {}
        self.cookies = cookies or {}


class Reply:
    """
    Simple transport reply representation.
    """

    def __init__(self, status: int, headers: Dict[str, str], body: bytes):
        self.status = status
        self.headers = headers
        self.body = body


class Transport:
    """
    The transport interface.
    """

    def __init__(self):
        """
        Constructor.
        """
        pass

    def _build_opener(
        self,
        request: Request,
    ) -> urllib.request.OpenerDirector:
        """
        Build an opener that handles proxies and cookies.
        """
        handlers = []

        if request.proxies:
            handlers.append(urllib.request.ProxyHandler(request.proxies))

        if request.cookies:
            cookie_jar = http.cookiejar.CookieJar()
            for name, value in request.cookies.items():
                # Create a cookie for the request URL
                cookie = http.cookiejar.Cookie(
                    version=0,
                    name=name,
                    value=value,
                    port=None,
                    port_specified=False,
                    domain=request.url.split("//", 1)[-1].split("/", 1)[0],
                    domain_specified=True,
                    domain_initial_dot=False,
                    path="/",
                    path_specified=True,
                    secure=False,
                    expires=None,
                    discard=True,
                    comment=None,
                    comment_url=None,
                    rest={},
                    rfc2109=False,
                )
                cookie_jar.set_cookie(cookie)
            handlers.append(urllib.request.HTTPCookieProcessor(cookie_jar))

        opener = urllib.request.build_opener(*handlers)
        return opener

    def open(self, request: Request) -> Any:
        """
        Open the URL in the specified request.
        @param request: A transport request.
        @type request: Request
        @return: An input stream.
        @rtype: file-like object
        @raise TransportError: On all transport errors.
        """
        try:
            req = urllib.request.Request(
                request.url,
                method=request.method,
                headers=request.headers,
            )
            opener = self._build_opener(request)
            response = opener.open(req)
            return response
        except urllib.error.URLError as e:
            raise TransportError(
                f"Failed to open URL {request.url}: {e}") from e
        except Exception as e:
            raise TransportError(
                f"Unexpected error opening URL {request.url}: {e}") from e

    def send(self, request: Request) -> Reply:
        """
        Send SOAP message.  Implementations are expected to handle:
            - proxies
            - HTTP headers
            - cookies
            - sending message
            - brokering exceptions into TransportError
        @param request: A transport request.
        @type request: Request
        @return: The reply
        @rtype: Reply
        @raise TransportError: On all transport errors.
        """
        try:
            data = request.body
            if isinstance(data, str):
                data = data.encode("utf-8")

            req = urllib.request.Request(
                request.url,
                data=data,
                method=request.method,
                headers=request.headers,
            )
            opener = self._build_opener(request)
            response = opener.open(req)
            body = response.read()
            headers = dict(response.getheaders())
            status = response.getcode()
            return Reply(status=status, headers=headers, body=body)
        except urllib.error.HTTPError as e:
            body = e.read()
            headers = dict(e.headers)
            status = e.code
            return Reply(status=status, headers=headers, body=body)
        except urllib.error.URLError as e:
            raise TransportError(
                f"Failed to send request to {request.url}: {e}") from e
        except Exception as e:
            raise TransportError(
                f"Unexpected error sending request to {request.url}: {e}") from e
