
class Addr:

    def __init__(self, map):
        '''
        map is an AddrMap instance, used for scheduling expiries and
        updating the map.
        '''
        self.map = map
        self.expiry_call = None
        self.addr = None
        self.expiry_time = None

    def update(self, *args):
        '''
        deals with an update from Tor; see parsing logic in torcontroller
        '''
        # Example: args = (addr, expiry_time)
        if len(args) < 2:
            return
        addr, expiry_time = args[0], args[1]
        self.addr = addr
        self.expiry_time = expiry_time
        if self.expiry_call:
            self.expiry_call.cancel()
        # Schedule expiry using map's scheduler (assume map has callLater)
        self.expiry_call = self.map.callLater(expiry_time, self._expire)

    def _expire(self):
        '''
        callback done via callLater
        '''
        if self.addr in self.map:
            del self.map[self.addr]
        self.expiry_call = None
