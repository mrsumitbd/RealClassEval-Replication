
from requests.exceptions import RequestException
import requests


class TransportError(Exception):
    """Base class for transport-related exceptions."""
    pass


class Request:
    """Represents a transport request."""

    def __init__(self, url, message=None, headers=None):
        """
        Constructor.
        @param url: The URL to be accessed.
        @type url: str
        @param message: The message to be sent.
        @type message: str
        @param headers: The HTTP headers.
        @type headers: dict
        """
        self.url = url
        self.message = message
        self.headers = headers if headers is not None else {}


class Reply:
    """Represents a transport reply."""

    def __init__(self, status, message, headers=None):
        """
        Constructor.
        @param status: The HTTP status code.
        @type status: int
        @param message: The reply message.
        @type message: str
        @param headers: The HTTP headers.
        @type headers: dict
        """
        self.status = status
        self.message = message
        self.headers = headers if headers is not None else {}


class Transport:
    '''
    The transport I{interface}.
    '''

    def __init__(self):
        '''
        Constructor.
        '''
        pass

    def open(self, request):
        '''
        Open the url in the specified request.
        @param request: A transport request.
        @type request: L{Request}
        @return: An input stream.
        @rtype: stream
        @raise TransportError: On all transport errors.
        '''
        try:
            response = requests.get(
                request.url, headers=request.headers, stream=True)
            response.raise_for_status()
            return response.raw
        except RequestException as e:
            raise TransportError(str(e))

    def send(self, request):
        '''
        Send soap message.  Implementations are expected to handle:
            - proxies
            - I{http} headers
            - cookies
            - sending message
            - brokering exceptions into L{TransportError}
        @param request: A transport request.
        @type request: L{Request}
        @return: The reply
        @rtype: L{Reply}
        @raise TransportError: On all transport errors.
        '''
        try:
            response = requests.post(
                request.url, headers=request.headers, data=request.message)
            response.raise_for_status()
            return Reply(response.status_code, response.text, dict(response.headers))
        except RequestException as e:
            raise TransportError(str(e))
