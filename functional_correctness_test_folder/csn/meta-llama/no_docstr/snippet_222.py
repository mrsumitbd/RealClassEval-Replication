
import time
import logging


class Transport:

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.is_connected = False
        self.connection = None
        self.last_reconnect_attempt = time.time()
        self.logger = logging.getLogger(__name__)

        try:
            self.connect_to_gateway()
        except Exception as e:
            self.logger.error(f"Failed to connect to gateway: {e}")

    def connect_to_gateway(self):
        if not self.is_connected:
            try:
                self.connection = self.connect(self.gateway, self.timeout)
                self.is_connected = True
                self.logger.info("Connected to gateway")
            except Exception as e:
                self.logger.error(f"Failed to connect to gateway: {e}")
                self.is_connected = False

    def disconnect(self):
        if self.is_connected:
            try:
                if hasattr(self.connection, 'close'):
                    self.connection.close()
                self.is_connected = False
                self.logger.info("Disconnected from gateway")
            except Exception as e:
                self.logger.error(f"Failed to disconnect from gateway: {e}")

    def send(self, message):
        if not self.is_connected:
            current_time = time.time()
            if current_time - self.last_reconnect_attempt >= self.reconnect_timeout:
                self.last_reconnect_attempt = current_time
                self.connect_to_gateway()
            else:
                self.logger.warning(
                    "Not connected to gateway. Message not sent.")
                return

        try:
            if hasattr(self.connection, 'send'):
                self.connection.send(message)
            else:
                self.logger.error(
                    "Connection object does not have a 'send' method.")
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            self.is_connected = False
