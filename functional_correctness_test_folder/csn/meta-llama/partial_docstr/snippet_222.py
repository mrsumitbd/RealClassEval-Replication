
import time
import socket


class Transport:
    '''Handle gateway transport.
    I/O is allowed in this class. This class should host methods that
    are related to the gateway transport type.
    '''

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.socket = None
        self.last_reconnect_attempt = 0
        self.connect_to_gateway()

    def connect_to_gateway(self):
        if time.time() - self.last_reconnect_attempt < self.reconnect_timeout:
            return
        self.last_reconnect_attempt = time.time()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect(self.connect)
        except (ConnectionRefusedError, socket.timeout):
            self.socket = None

    def disconnect(self):
        '''Disconnect from the transport.'''
        if self.socket:
            self.socket.close()
            self.socket = None

    def send(self, message):
        '''Write a message to the gateway.'''
        if not self.socket:
            self.connect_to_gateway()
            if not self.socket:
                return
        try:
            self.socket.sendall(message.encode())
        except (ConnectionResetError, BrokenPipeError, socket.timeout):
            self.disconnect()
