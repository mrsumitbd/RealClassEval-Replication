
import time


class Addr:
    def __init__(self, map):
        """
        Initialize the Addr instance.

        Parameters
        ----------
        map : dict
            The underlying dictionary to store address entries.
        """
        self.map = map
        # Store expiration times for keys that have a TTL
        self._expire_map = {}

    def update(self, *args):
        """
        Update the address map with new entries.

        The method accepts either:
          - key, value
          - key, value, ttl (time-to-live in seconds)

        Parameters
        ----------
        *args : tuple
            Variable length argument list.
        """
        if len(args) == 2:
            key, value = args
            ttl = None
        elif len(args) == 3:
            key, value, ttl = args
        else:
            raise TypeError(
                "update() takes 2 or 3 positional arguments (got {})".format(len(args)))

        # Update the map
        self.map[key] = value

        # Handle TTL
        if ttl is not None:
            self._expire_map[key] = time.time() + ttl
        else:
            self._expire_map.pop(key, None)

        # Remove any expired entries
        self._expire()

    def _expire(self):
        """
        Remove entries from the map that have expired.
        """
        now = time.time()
        expired_keys = [k for k, exp in self._expire_map.items() if exp <= now]
        for k in expired_keys:
            self.map.pop(k, None)
            self._expire_map.pop(k, None)
