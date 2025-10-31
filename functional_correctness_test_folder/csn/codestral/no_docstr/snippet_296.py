
class NameServer:

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):

        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self.server = None

    def run(self, address_receiver=None, nameserver_address=None):

        if self.server is not None:
            raise RuntimeError("Server is already running")

        if address_receiver is None:
            def address_receiver(address): return print(
                f"Received address: {address}")

        if nameserver_address is None:
            nameserver_address = (
                '', 5353) if not self.restrict_to_localhost else ('127.0.0.1', 5353)

        import socketserver
        import threading

        class UDPHandler(socketserver.BaseRequestHandler):

            def handle(self):
                data = self.request[0].strip()
                socket = self.request[1]
                address_receiver(data.decode('utf-8'))

        self.server = socketserver.UDPServer(nameserver_address, UDPHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def stop(self):

        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
            self.server_thread.join()
            self.server = None
