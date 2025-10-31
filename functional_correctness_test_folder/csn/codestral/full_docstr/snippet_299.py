
class _AddressListener:
    '''Listener for new addresses of interest.'''

    def __init__(self, subscriber, services='', nameserver='localhost'):
        '''Initialize address listener.'''
        self.subscriber = subscriber
        self.services = services
        self.nameserver = nameserver

    def handle_msg(self, msg):
        '''Handle the message *msg*.'''
        if msg.type == 'new_address':
            self.subscriber.add_address(msg.address, msg.port, self.services)
