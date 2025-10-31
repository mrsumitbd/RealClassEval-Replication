from posttroll.backends.zmq.socket import SocketReceiver, close_socket, set_up_client_socket, set_up_server_socket
from contextlib import suppress
from zmq import LINGER, REP, REQ
from posttroll.ns import get_active_address, get_configured_nameserver_port

class ZMQNameServer:
    """The name server."""

    def __init__(self):
        """Set up the nameserver."""
        self.running: bool = True
        self.listener: SocketReceiver | None = None
        self._authenticator = None

    def run(self, address_receiver, address: str | None=None):
        """Run the listener and answer to requests."""
        port = get_configured_nameserver_port()
        try:
            if not self.running:
                return
            if address is None:
                address = '*'
            address = create_nameserver_address(address)
            self.listener, _, self._authenticator = set_up_server_socket(REP, address)
            logger.debug(f'Nameserver listening on port {port}')
            socket_receiver = SocketReceiver()
            socket_receiver.register(self.listener)
            while self.running:
                try:
                    for msg, _ in socket_receiver.receive(self.listener, timeout=1):
                        logger.debug('Replying to request: ' + str(msg))
                        active_address = get_active_address(msg.data['service'], address_receiver, msg.version)
                        self.listener.send_unicode(str(active_address))
                except TimeoutError:
                    continue
        except KeyboardInterrupt:
            pass
        finally:
            socket_receiver.unregister(self.listener)
            self.close_sockets_and_threads()

    def close_sockets_and_threads(self):
        """Close all sockets and threads."""
        with suppress(AttributeError):
            close_socket(self.listener)
        with suppress(AttributeError):
            self._authenticator.stop()

    def stop(self):
        """Stop the name server."""
        self.running = False