
import json
import socket
import struct
import threading
import time
from typing import Callable, Dict, Optional, Tuple


class NameServer:
    """
    A very small, UDP‑based name server that supports optional multicast,
    optional restriction to localhost, and optional TTL for registrations.
    """

    def __init__(
        self,
        max_age: Optional[float] = None,
        multicast_enabled: bool = True,
        restrict_to_localhost: bool = False,
    ):
        """
        Parameters
        ----------
        max_age : float | None
            Maximum age (in seconds) of a registration before it is considered
            expired. If None, registrations never expire.
        multicast_enabled : bool
            If True, the server will join the multicast group 224.0.0.251
            (mDNS) and listen for multicast packets.
        restrict_to_localhost : bool
            If True, the server will only accept packets from the local host.
        """
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost

        # Internal state
        # name -> (address, timestamp)
        self._registry: Dict[str, Tuple[str, float]] = {}
        self._sock: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #

    def run(
        self,
        address_receiver: Optional[Callable[[
            bytes, Tuple[str, int]], None]] = None,
        nameserver_address: Optional[Tuple[str, int]] = None,
    ) -> None:
        """
        Start the name server.

        Parameters
        ----------
        address_receiver : callable | None
            Optional callback that receives raw data and the sender address.
            It is called *after* the server has processed the packet.
        nameserver_address : tuple | None
            Address to bind to. If None, defaults to ('0.0.0.0', 5353).
        """
        if self._thread and self._thread.is_alive():
            raise RuntimeError("NameServer is already running")

        bind_addr = nameserver_address or ("0.0.0.0", 5353)
        self._sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(bind_addr)

        if self.multicast_enabled:
            # Join the mDNS multicast group
            mcast_group = socket.inet_aton("224.0.0.251")
            mreq = mcast_group + socket.inet_aton("0.0.0.0")
            self._sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._serve_loop,
            args=(address_receiver,),
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the name server and close the socket.
        """
        if not self._thread:
            return
        self._stop_event.set()
        # Send an empty packet to unblock the socket if it's waiting
        try:
            dummy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dummy_sock.sendto(b"", ("127.0.0.1", self._sock.getsockname()[1]))
            dummy_sock.close()
        except Exception:
            pass
        self._thread.join()
        self._thread = None
        if self._sock:
            self._sock.close()
            self._sock = None

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #

    def _serve_loop(self, address_receiver: Optional[Callable[[bytes, Tuple[str, int]], None]]) -> None:
        sock = self._sock
        if not sock:
            return

        while not self._stop_event.is_set():
            try:
                data, addr = sock.recvfrom(4096)
            except OSError:
                break

            if self.restrict_to_localhost and addr[0] != "127.0.0.1":
                continue

            try:
                msg = json.loads(data.decode("utf-8"))
            except Exception:
                # Malformed packet; ignore
                continue

            action = msg.get("action")
            if action == "register":
                name = msg.get("name")
                address = msg.get("address")
                if name and address:
                    self._registry[name] = (address, time.time())
                    response = {"status": "ok"}
                else:
                    response = {"status": "error",
                                "message": "invalid register payload"}
            elif action == "lookup":
                name = msg.get("name")
                if name:
                    entry = self._registry.get(name)
                    if entry:
                        address, ts = entry
                        if self.max_age is None or (time.time() - ts) <= self.max_age:
                            response = {"status": "ok", "address": address}
                        else:
                            # Expired
                            del self._registry[name]
                            response = {"status": "error",
                                        "message": "name expired"}
                    else:
                        response = {"status": "error",
                                    "message": "name not found"}
                else:
                    response = {"status": "error",
                                "message": "invalid lookup payload"}
            else:
                response = {"status": "error", "message": "unknown action"}

            # Send response
            try:
                sock.sendto(json.dumps(response).encode("utf-8"), addr)
            except Exception:
                pass

            # Call optional receiver callback
            if address_receiver:
                try:
                    address_receiver(data, addr)
                except Exception:
                    pass
