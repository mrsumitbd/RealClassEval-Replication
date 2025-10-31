
class _AddressListener:
    '''Listener for new addresses of interest.'''

    def __init__(self, subscriber, services='', nameserver='localhost'):
        '''Initialize address listener.'''
        self.subscriber = subscriber
        # Normalize services to a list of strings
        if isinstance(services, str):
            self.services = [services] if services else []
        else:
            self.services = list(services)
        self.nameserver = nameserver

    def handle_msg(self, msg):
        '''Handle the message *msg*.'''
        # Expect msg to be a mapping with at least 'service' and 'address'
        service = msg.get('service')
        if self.services and service not in self.services:
            return  # ignore services we are not interested in

        address = msg.get('address')
        name = msg.get('name')
        # Call the subscriber callback with the relevant information
        self.subscriber(address, name, service)
