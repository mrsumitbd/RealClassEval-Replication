from abc import ABC, abstractmethod


class Transport(ABC):
    '''
    The transport interface.
    '''

    def __init__(self):
        '''
        Constructor.
        '''
        super().__init__()

    @abstractmethod
    def open(self, request):
        '''
        Open the url in the specified request.
        @param request: A transport request.
        @type request: L{Request}
        @return: An input stream.
        @rtype: stream
        @raise TransportError: On all transport errors.
        '''
        raise NotImplementedError("open() must be implemented by subclasses")

    @abstractmethod
    def send(self, request):
        '''
        Send soap message.  Implementations are expected to handle:
            - proxies
            - http headers
            - cookies
            - sending message
            - brokering exceptions into L{TransportError}
        @param request: A transport request.
        @type request: L{Request}
        @return: The reply
        @rtype: L{Reply}
        @raise TransportError: On all transport errors.
        '''
        raise NotImplementedError("send() must be implemented by subclasses")
