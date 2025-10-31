
class _AddressListener:

    def __init__(self, subscriber, services='', nameserver='localhost'):
        self.subscriber = subscriber
        self.services = services
        self.nameserver = nameserver

    def handle_msg(self, msg):
        # Assuming msg is a dictionary with 'address' and 'service' keys
        if msg.get('service') in self.services:
            self.subscriber.update_address(msg['address'])
