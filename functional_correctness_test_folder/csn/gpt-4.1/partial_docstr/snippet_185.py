
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
        raise NotImplementedError("Subclasses must implement 'open' method.")

    def send(self, request):
        raise NotImplementedError("Subclasses must implement 'send' method.")
