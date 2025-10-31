
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
        Open the transport connection.

        :param request: The request to open the connection.
        '''
        raise NotImplementedError("Subclasses must implement this method")

    def send(self, request):
        '''
        Send a request over the transport connection.

        :param request: The request to send.
        '''
        raise NotImplementedError("Subclasses must implement this method")
