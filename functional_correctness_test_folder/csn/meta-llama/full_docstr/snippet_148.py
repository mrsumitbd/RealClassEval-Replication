
from twisted.internet import reactor


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
        self.delayed_call = None

    def update(self, *args):
        '''
        deals with an update from Tor; see parsing logic in torcontroller
        '''
        if self.delayed_call is not None and self.delayed_call.active():
            self.delayed_call.cancel()
        self.map.update(self, *args)
        self.delayed_call = reactor.callLater(self.map.ttl, self._expire)

    def _expire(self):
        '''
        callback done via callLater
        '''
        self.map.expire(self)
