
import urllib.request
import urllib.error


class TransportError(Exception):
    pass


class Request:
    def __init__(self, url, data=None, headers=None):
        self.url = url
        self.data = data
        self.headers = headers or {}


class Reply:
    def __init__(self, status_code, content, headers=None):
        self.status_code = status_code
        self.content = content
        self.headers = headers or {}


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
            req = urllib.request.Request(request.url, headers=request.headers)
            return urllib.request.urlopen(req)
        except Exception as e:
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
            data = request.data
            if data is not None and not isinstance(data, bytes):
                data = data.encode('utf-8')
            req = urllib.request.Request(
                request.url, data=data, headers=request.headers)
            with urllib.request.urlopen(req) as response:
                content = response.read()
                status_code = response.getcode()
                headers = dict(response.getheaders())
                return Reply(status_code, content, headers)
        except Exception as e:
            raise TransportError(str(e))
