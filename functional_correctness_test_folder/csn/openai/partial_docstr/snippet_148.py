
import threading
from datetime import datetime, timedelta


class Addr:
    """
    Represents a Tor address that can be updated and automatically expires.
    The `map` argument is an instance of AddrMap (or any mapping-like object)
    that is responsible for storing and removing Addr objects.
    """

    def __init__(self, map):
        """
        Initialise the Addr instance.

        Parameters
        ----------
        map : AddrMap
            The map that holds this Addr. It is used to schedule expiries
            and to update the map when the address changes.
        """
        self.map = map
        # the address string (e.g. "127.0.0.1:9050")
        self.address = None
        self.expire_time = None      # UTC datetime when this Addr should expire
        self._timer = None           # threading.Timer used for expiry
        self._lock = threading.Lock()  # protects concurrent access

    def update(self, *args):
        """
        Update the address information.

        The first argument is expected to be the address string.
        The second optional argument is the number of seconds until
        the address should expire.  If the expiry argument is omitted,
        the address will not expire automatically.

        Parameters
        ----------
        *args : tuple
            Variable length argument list.  At least one element
            (the address) is required.
        """
        if not args:
            return

        with self._lock:
            # Parse arguments
            address = args[0]
            expires_in = args[1] if len(args) > 1 else None

            # Store the new address
            self.address = address

            # Cancel any existing timer
            if self._timer:
                self._timer.cancel()
                self._timer = None

            # Schedule a new expiry if requested
            if expires_in is not None:
                self.expire_time = datetime.utcnow() + timedelta(seconds=expires_in)
                self._timer = threading.Timer(expires_in, self._expire)
                self._timer.daemon = True
                self._timer.start()
            else:
                self.expire_time = None

            # Notify the map that this Addr has been updated
            if hasattr(self.map, "update"):
                # The map may expect the Addr instance itself
                self.map.update(self)
            else:
                # Fallback: store the Addr in a plain dict
                self.map[self.address] = self

    def _expire(self):
        """
        Internal callback invoked when the address expires.
        Removes the Addr from the map and cleans up internal state.
        """
        with self._lock:
            # Remove from the map
            if hasattr(self.map, "expire"):
                self.map.expire(self)
            else:
                # Fallback: remove from a plain dict
                self.map.pop(self.address, None)

            # Clean up timer and expiry time
            self._timer = None
            self.expire_time = None
