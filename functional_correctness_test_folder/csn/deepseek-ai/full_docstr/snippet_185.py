
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
        raise NotImplementedError("Method 'open' must be implemented.")

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
        raise NotImplementedError("Method 'send' must be implemented.")
