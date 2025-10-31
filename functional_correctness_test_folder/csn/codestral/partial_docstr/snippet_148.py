
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
        if self.expiry is not None:
            self.expiry.cancel()
        self.expiry = reactor.callLater(60, self._expire)
        self.map.update(self, *args)

    def _expire(self):
        '''
        callback done via callLater
        '''
        self.map.expire(self)
