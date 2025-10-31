
import threading
import time


class Addr:
    """
    One address mapping (e.g. example.com -> 127.0.0.1)
    """

    def __init__(self, map):
        """
        map is an AddrMap instance, used for scheduling expiries and
        updating the map.
        """
        self.map = map
        self.domain = None
        self.ip = None
        self._timer = None
        self.expired = False

    def update(self, *args):
        """
        deals with an update from Tor; see parsing logic in torcontroller
        Expected args: (domain, ip, ttl)
        """
        if len(args) < 3:
            return

        domain, ip, ttl = args[0], args[1], args[2]
        self.domain = domain
        self.ip = ip

        # cancel any existing expiry timer
        if self._timer is not None:
            try:
                self._timer.cancel()
            except Exception:
                pass
            self._timer = None

        # schedule new expiry if ttl is provided
        try:
            ttl = int(ttl)
        except Exception:
            ttl = None

        if ttl:
            self._timer = threading.Timer(ttl, self._expire)
            self._timer.daemon = True
            self._timer.start()

        # inform the map about the new mapping
        if hasattr(self.map, "update_mapping"):
            self.map.update_mapping(self)
        else:
            # fallback: assume map behaves like a dict
            self.map[self.domain] = self.ip

    def _expire(self):
        """
        callback done via callLater
        """
        self.expired = True
        if hasattr(self.map, "remove"):
            self.map.remove(self)
        else:
            # fallback: assume map behaves like a dict
            self.map.pop(self.domain, None)
