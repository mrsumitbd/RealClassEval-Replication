
import zmq
import time

# Assuming _MAGICK is a predefined constant or variable
_MAGICK = b''  # Replace with actual value


class Subscribe:

    def __init__(self, services='', topics=_MAGICK, addr_listener=False, addresses=None, timeout=10, translate=False, nameserver='localhost', message_filter=None):
        self.context = zmq.Context()
        self.services = services.split(',')
        self.topics = topics
        self.addr_listener = addr_listener
        self.addresses = addresses if addresses else []
        self.timeout = timeout
        self.translate = translate
        self.nameserver = nameserver
        self.message_filter = message_filter
        self.socket = None

    def __enter__(self):
        self.socket = self.context.socket(zmq.SUB)
        if self.addr_listener:
            for address in self.addresses:
                self.socket.connect(address)
        else:
            # Assuming a nameserver is used to get the addresses
            # Replace with actual implementation to get addresses from nameserver
            addresses = self.get_addresses_from_nameserver()
            for address in addresses:
                self.socket.connect(address)

        if isinstance(self.topics, list):
            for topic in self.topics:
                self.socket.setsockopt(zmq.SUBSCRIBE, topic)
        else:
            self.socket.setsockopt(zmq.SUBSCRIBE, self.topics)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.socket:
            self.socket.close()
        self.context.term()

    def get_addresses_from_nameserver(self):
        # Replace with actual implementation to get addresses from nameserver
        # For demonstration purposes, assume it returns a list of addresses
        return ['tcp://localhost:5555']  # Replace with actual addresses

    def receive(self):
        if self.socket:
            try:
                message = self.socket.recv(timeout=self.timeout*1000)
                if self.message_filter:
                    return self.message_filter(message)
                return message
            except zmq.Again:
                return None
        return None


# Example usage:
if __name__ == "__main__":
    with Subscribe(services='service1', topics=b'topic1', addr_listener=True, addresses=['tcp://localhost:5555']) as subscriber:
        while True:
            message = subscriber.receive()
            if message:
                print(message)
            else:
                print("No message received")
                break
            time.sleep(1)
