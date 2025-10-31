
class _AddressListener:
    '''Listener for new addresses of interest.'''

    def __init__(self, subscriber, services='', nameserver='localhost'):
        '''Initialize address listener.'''
        self.subscriber = subscriber
        self.services = services
        self.nameserver = nameserver
        self.addresses = []

    def handle_msg(self, msg):
        '''Handle the message *msg*.'''
        # Assume msg is a dict with 'address' key
        address = msg.get('address')
        if address and address not in self.addresses:
            self.addresses.append(address)
            # Notify the subscriber about the new address
            if hasattr(self.subscriber, 'notify'):
                self.subscriber.notify(address)
