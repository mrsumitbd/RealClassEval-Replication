
class Transport:

    def __init__(self):
        self.is_open = False

    def open(self, request):
        if not self.is_open:
            print(f"Opening connection for {request}")
            self.is_open = True
        else:
            print("Connection is already open")

    def send(self, request):
        if self.is_open:
            print(f"Sending {request}")
        else:
            raise Exception("Connection is not open")
