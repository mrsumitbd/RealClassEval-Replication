
class _AddressListener:

    def __init__(self, subscriber, services='', nameserver='localhost'):
        self.subscriber = subscriber
        self.services = services
        self.nameserver = nameserver
        self.messages = []

    def handle_msg(self, msg):
        # Store the message and notify the subscriber
        self.messages.append(msg)
        if hasattr(self.subscriber, 'notify'):
            self.subscriber.notify(msg)
        elif callable(self.subscriber):
            self.subscriber(msg)
