
import time
import logging


class Transport:
    '''Handle gateway transport.
    I/O is allowed in this class. This class should host methods that
    are related to the gateway transport type.
    '''

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        '''Set up transport.'''
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.is_connected = False
        self.last_reconnect_attempt = 0
        self.logger = logging.getLogger(__name__)

        if self.connect:
            self._connect()

    def _connect(self):
        try:
            # Assuming the gateway has a connect method
            self.gateway.connect()
            self.is_connected = True
            self.logger.info("Connected to gateway")
        except Exception as e:
            self.logger.error(f"Failed to connect to gateway: {e}")
            self.is_connected = False

    def disconnect(self):
        '''Disconnect from the transport.'''
        if self.is_connected:
            try:
                # Assuming the gateway has a disconnect method
                self.gateway.disconnect()
                self.is_connected = False
                self.logger.info("Disconnected from gateway")
            except Exception as e:
                self.logger.error(f"Failed to disconnect from gateway: {e}")

    def _reconnect(self):
        current_time = time.time()
        if current_time - self.last_reconnect_attempt >= self.reconnect_timeout:
            self.last_reconnect_attempt = current_time
            self._connect()

    def send(self, message):
        '''Write a message to the gateway.'''
        if not self.is_connected:
            self._reconnect()
            if not self.is_connected:
                self.logger.error(
                    "Not connected to gateway, cannot send message")
                return

        try:
            # Assuming the gateway has a send method
            self.gateway.send(message, timeout=self.timeout)
            self.logger.debug(f"Sent message to gateway: {message}")
        except Exception as e:
            self.logger.error(f"Failed to send message to gateway: {e}")
            self.is_connected = False
