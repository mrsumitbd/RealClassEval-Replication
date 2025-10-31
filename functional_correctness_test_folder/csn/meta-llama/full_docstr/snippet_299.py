
import zmq
import json


class _AddressListener:
    '''Listener for new addresses of interest.'''

    def __init__(self, subscriber, services='', nameserver='localhost'):
        '''Initialize address listener.'''
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect(f"tcp://{nameserver}:5556")
        if services:
            for service in services.split(','):
                self.subscriber.setsockopt(
                    zmq.SUBSCRIBE, service.encode('utf-8'))
        else:
            self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')

    def handle_msg(self, msg):
        '''Handle the message *msg*.'''
        try:
            data = json.loads(msg.decode('utf-8'))
            service = data.get('service')
            address = data.get('address')
            if service and address:
                self.subscriber_callback(service, address)
        except json.JSONDecodeError:
            pass

    def subscriber_callback(self, service, address):
        # This method should be overridden by the subscriber
        self.subscriber.setsockopt(zmq.SUBSCRIBE, service.encode('utf-8'))
        if hasattr(self.subscriber, 'callback'):
            self.subscriber.callback(service, address)

    def start_listening(self):
        while True:
            try:
                msg = self.subscriber.recv(zmq.NOBLOCK)
                self.handle_msg(msg[message_length:])
            except zmq.ZMQError:
                pass

    def run(self):
        # get the length of the first message to determine the length of subsequent messages
        message_length = len(self.subscriber.recv(zmq.NOBLOCK))
        # discard the first message as it is used to get the length
        self.subscriber.recv(zmq.NOBLOCK)
        while True:
            try:
                msg = self.subscriber.recv()
                self.handle_msg(msg[message_length:])
            except zmq.ZMQError as e:
                print(f"Error: {e}")
