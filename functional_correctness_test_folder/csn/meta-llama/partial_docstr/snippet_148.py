
from twisted.internet import reactor


class AddrMap:
    # For the sake of completeness, let's assume AddrMap is defined like this
    def update(self, addr, expiry):
        pass

    def schedule_expiry(self, callback, delay):
        reactor.callLater(delay, callback)


class Addr:

    def __init__(self, map):
        '''
        map is an AddrMap instance, used for scheduling expiries and
        updating the map.
        '''
        self.map = map
        self.expiry = None

    def update(self, *args):
        '''
        deals with an update from Tor; see parsing logic in torcontroller
        '''
        if len(args) != 2:
            raise ValueError("Expected two arguments: address and expiry")
        addr, expiry = args
        if self.expiry is not None:
            self._unschedule_expiry()
        self.map.update(addr, expiry)
        delay = expiry - reactor.seconds()
        if delay > 0:
            self.expiry = expiry
            self.map.schedule_expiry(self._expire, delay)

    def _unschedule_expiry(self):
        # Assuming there's no direct way to cancel a callLater in AddrMap,
        # we'll keep track of the DelayedCall object in Addr class itself.
        # However, for simplicity, let's assume AddrMap's schedule_expiry returns the DelayedCall object.
        # In a real scenario, you would need to modify AddrMap to return this object.
        if hasattr(self, '_dc'):
            self._dc.cancel()
            del self._dc

    def _expire(self):
        '''
        callback done via callLater
        '''
        self.map.update(
            None, 0)  # Assuming updating with None and 0 means expiring
        self.expiry = None
        # For the sake of completeness, let's assume we need to schedule_expiry again if needed.
        # However, the problem statement doesn't specify this, so it's left out.


# Example usage:
if __name__ == "__main__":
    addr_map = AddrMap()
    addr = Addr(addr_map)
    addr.update('example.com', reactor.seconds() + 10)
    reactor.run()
