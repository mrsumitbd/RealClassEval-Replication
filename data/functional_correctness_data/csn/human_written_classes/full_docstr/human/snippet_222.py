class Transport:
    """Handle gateway transport.

    I/O is allowed in this class. This class should host methods that
    are related to the gateway transport type.
    """

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        """Set up transport."""
        self._connect = connect
        self.can_log = False
        self.connect_task = None
        self.gateway = gateway
        self.protocol = None
        self.reconnect_timeout = reconnect_timeout
        self.timeout = timeout

    def disconnect(self):
        """Disconnect from the transport."""
        if not self.protocol or not self.protocol.transport:
            self.protocol = None
            return
        _LOGGER.info('Disconnecting from gateway')
        self.protocol.transport.close()
        self.protocol = None

    def send(self, message):
        """Write a message to the gateway."""
        if not message or not self.protocol or (not self.protocol.transport):
            return
        if not self.can_log:
            _LOGGER.debug('Sending %s', message.strip())
        try:
            self.protocol.transport.write(message.encode())
        except OSError as exc:
            _LOGGER.error('Failed writing to transport %s: %s', self.protocol.transport, exc)
            self.protocol.transport.close()
            self.protocol.conn_lost_callback()