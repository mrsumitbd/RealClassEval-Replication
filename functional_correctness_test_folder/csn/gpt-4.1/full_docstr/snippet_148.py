
class Addr:
    '''
    One address mapping (e.g. example.com -> 127.0.0.1)
    '''

    def __init__(self, map):
        '''
        map is an AddrMap instance, used for scheduling expiries and
        updating the map.
        '''
        self.map = map
        self.hostname = None
        self.address = None
        self.expiry = None
        self._expire_call = None

    def update(self, hostname, address, expiry=None):
        '''
        deals with an update from Tor; see parsing logic in torcontroller
        '''
        self.hostname = hostname
        self.address = address
        self.expiry = expiry
        # Cancel previous expiry if any
        if self._expire_call is not None:
            try:
                self._expire_call.cancel()
            except Exception:
                pass
            self._expire_call = None
        # Schedule new expiry if expiry is set
        if expiry is not None and hasattr(self.map, 'callLater'):
            from time import time
            delay = expiry - time()
            if delay > 0:
                self._expire_call = self.map.callLater(delay, self._expire)

    def _expire(self):
        '''
        callback done via callLater
        '''
        if hasattr(self.map, 'remove'):
            self.map.remove(self.hostname)
        self._expire_call = None
