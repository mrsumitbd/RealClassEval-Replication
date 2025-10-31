
class _AddressListener:

    def __init__(self, subscriber, services='', nameserver='localhost'):
        self.subscriber = subscriber
        self.services = services
        self.nameserver = nameserver

    def handle_msg(self, msg):
        pass
