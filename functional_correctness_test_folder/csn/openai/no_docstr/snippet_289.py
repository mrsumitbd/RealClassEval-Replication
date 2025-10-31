
import zmq
import threading
import time


class ZMQDesignatedReceiversSender:
    """
    A simple ZeroMQ sender that can send data to a set of designated receivers.
    Each receiver is identified by a name and an address. The sender creates a
    PUSH socket for each receiver and connects to the given address.
    """

    def __init__(self, default_port, receivers):
        """
        Parameters
        ----------
        default_port : int
            Default port to use if a receiver address does not specify a port.
        receivers : dict
            Mapping of receiver name to address string. The address may be a
            full ZeroMQ endpoint (e.g. "tcp://127.0.0.1:5555") or just a host
            (e.g. "127.0.0.1") in which case the default_port is appended.
        """
        self._default_port = default_port
        self._receivers = receivers
        self._context = zmq.Context.instance()
        self._sockets = {}
        self._lock = threading.Lock()

        for name, addr in receivers.items():
            # Ensure the address contains a port
            if "://" not in addr:
                addr = f"tcp://{addr}"
            if ":" not in addr.split("://")[1]:
                addr = f"{addr}:{self._default_port}"
            socket = self._context.socket(zmq.PUSH)
            socket.setsockopt(zmq.LINGER, 0)
            socket.connect(addr)
            self._sockets[name] = socket

    def __call__(self, data):
        """
        Send the given data to all configured receivers.

        Parameters
        ----------
        data : any
            The Python object to send. It will be serialized with zmq.send_pyobj.
        """
        with self._lock:
            for name, sock in self._sockets.items():
                try:
                    sock.send_pyobj(data, flags=zmq.NOBLOCK)
                except zmq.Again:
                    # If the socket is blocked, we can optionally retry or drop.
                    # Here we simply drop the message.
                    pass

    def _send_to_address(self, address, data, timeout=10):
        """
        Send data to a specific address. This method is not used by __call__
        but can be used for targeted sending.

        Parameters
        ----------
        address : str
            ZeroMQ endpoint to send to.
        data : any
            The Python object to send.
        timeout : int, optional
            Timeout in seconds for the send operation.
        """
        # Create a temporary socket for one-shot send
        sock = self._context.socket(zmq.PUSH)
        sock.setsockopt(zmq.LINGER, 0)
        sock.setsockopt(zmq.SNDTIMEO, int(timeout * 1000))
        sock.connect(address)
        try:
            sock.send_pyobj(data, flags=zmq.NOBLOCK)
        except zmq.Again:
            # Timeout or blocked
            pass
        finally:
            sock.close()

    def close(self):
        """
        Close all sockets and terminate the ZeroMQ context.
        """
        with self._lock:
            for sock in self._sockets.values():
                try:
                    sock.close()
                except Exception:
                    pass
            self._sockets.clear()
        # Do not terminate the context if it was shared
        # (Context.instance() is used). If you want to terminate
        # the context, uncomment the following line:
        # self._context.term()
