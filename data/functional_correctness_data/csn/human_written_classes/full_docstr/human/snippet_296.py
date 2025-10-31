from posttroll.address_receiver import AddressReceiver
import datetime as dt
from posttroll import config
from contextlib import suppress

class NameServer:
    """The name server."""

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        """Initialize nameserver."""
        self.loop = True
        self.listener = None
        self._max_age = max_age or dt.timedelta(minutes=10)
        self._multicast_enabled = multicast_enabled
        self._restrict_to_localhost = restrict_to_localhost
        backend = config['backend']
        if backend not in ['unsecure_zmq', 'secure_zmq']:
            raise NotImplementedError(f'Did not recognize backend: {backend}')
        from posttroll.backends.zmq.ns import ZMQNameServer
        self._ns = ZMQNameServer()

    def run(self, address_receiver=None, nameserver_address=None):
        """Run the listener and answer to requests."""
        if address_receiver is None:
            address_receiver = AddressReceiver(max_age=self._max_age, multicast_enabled=self._multicast_enabled, restrict_to_localhost=self._restrict_to_localhost)
            address_receiver.start()
        try:
            return self._ns.run(address_receiver, nameserver_address)
        finally:
            with suppress(AttributeError):
                address_receiver.stop()

    def stop(self):
        """Stop the nameserver."""
        return self._ns.stop()