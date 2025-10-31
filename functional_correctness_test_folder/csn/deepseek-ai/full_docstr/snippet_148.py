
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
        self.expiry_call = None

    def update(self, *args):
        '''
        deals with an update from Tor; see parsing logic in torcontroller
        '''
        if self.expiry_call and self.expiry_call.active():
            self.expiry_call.cancel()
        self.expiry_call = self.map.reactor.callLater(
            self.map.ttl, self._expire)

    def _expire(self):
        '''
        callback done via callLater
        '''
        self.map.remove(self)
