
class TransportError(Exception):
    """Custom exception for transport errors."""
    pass


class Request:
    """Class representing a transport request."""

    def __init__(self, url, headers=None, cookies=None, data=None, proxies=None):
        self.url = url
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.data = data
        self.proxies = proxies or {}


class Reply:
    """Class representing a transport reply."""

    def __init__(self, status_code, headers, content):
        self.status_code = status_code
        self.headers = headers
        self.content = content


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
            import requests
            response = requests.get(
                request.url, headers=request.headers, cookies=request.cookies, proxies=request.proxies)
            response.raise_for_status()
            return response.raw
        except Exception as e:
            raise TransportError(f"Failed to open URL: {e}")

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
            import requests
            response = requests.post(request.url, headers=request.headers,
                                     cookies=request.cookies, data=request.data, proxies=request.proxies)
            response.raise_for_status()
            return Reply(response.status_code, response.headers, response.content)
        except Exception as e:
            raise TransportError(f"Failed to send message: {e}")
