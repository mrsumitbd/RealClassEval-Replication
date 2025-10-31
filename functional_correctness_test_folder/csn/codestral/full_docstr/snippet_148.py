
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
        self.address = None
        self.expiry = None

    def update(self, *args):
        '''
        deals with an update from Tor; see parsing logic in torcontroller
        '''
        if len(args) >= 2:
            self.address = args[1]
            if len(args) >= 3:
                self.expiry = args[2]
                self.map.schedule_expiry(self, self.expiry)

    def _expire(self):
        '''
        callback done via callLater
        '''
        self.map.remove(self)
