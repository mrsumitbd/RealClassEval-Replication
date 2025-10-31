
class NameServer:
    '''The name server.'''

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self.server = None

    def run(self, address_receiver=None, nameserver_address=None):
        from zeroconf import ServiceInfo, Zeroconf
        import socket

        if self.restrict_to_localhost:
            nameserver_address = ('127.0.0.1', 5353)

        self.server = Zeroconf()

        if address_receiver:
            address_receiver(self.server)

        if nameserver_address:
            info = ServiceInfo("_http._tcp.local.",
                               "My Service._http._tcp.local.",
                               addresses=[socket.inet_aton(
                                   nameserver_address[0])],
                               port=nameserver_address[1],
                               properties={})
            self.server.register_service(info)

    def stop(self):
        if self.server:
            self.server.close()
