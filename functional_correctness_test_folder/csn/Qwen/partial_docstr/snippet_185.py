
class Transport:
    '''
    The transport I{interface}.
    '''

    def __init__(self):
        '''
        Constructor.
        '''
        self.connection = None

    def open(self, request):
        # Simulate opening a connection
        self.connection = request
        print(f"Connection opened with request: {request}")

    def send(self, request):
        # Simulate sending data
        if self.connection:
            print(
                f"Sending request: {request} over connection: {self.connection}")
        else:
            print("No connection open. Please open a connection first.")
