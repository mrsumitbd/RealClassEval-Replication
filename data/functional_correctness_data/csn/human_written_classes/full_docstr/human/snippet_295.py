from posttroll import config, message

class DesignatedReceiversSender:
    """Sends message to multiple *receivers* on *port*."""

    def __init__(self, default_port, receivers):
        """Set settings."""
        backend = config.get('backend', 'unsecure_zmq')
        if backend == 'unsecure_zmq':
            from posttroll.backends.zmq.message_broadcaster import ZMQDesignatedReceiversSender
            self._sender = ZMQDesignatedReceiversSender(default_port, receivers)
        else:
            raise NotImplementedError()

    def __call__(self, data):
        """Send messages from all receivers."""
        return self._sender(data)

    def close(self):
        """Close the sender."""
        return self._sender.close()