
class _AddressListener:

    def __init__(self, subscriber, services='', nameserver='localhost'):
        '''Initialize address listener.'''
        self.subscriber = subscriber
        self.services = services
        self.nameserver = nameserver
        self.messages = []

    def handle_msg(self, msg):
        '''Handle the message *msg*.'''
        # For demonstration, store the message and notify the subscriber
        self.messages.append(msg)
        if hasattr(self.subscriber, 'notify'):
            self.subscriber.notify(msg)
