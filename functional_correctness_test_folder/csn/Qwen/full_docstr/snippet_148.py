
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
        self.expiry_time = None
        self.address = None

    def update(self, *args):
        '''
        deals with an update from Tor; see parsing logic in torcontroller
        '''
        if args:
            self.address = args[0]
            self.expiry_time = args[1]
            self.map.schedule_expiry(self, self.expiry_time)

    def _expire(self):
        '''
        callback done via callLater
        '''
        self.map.remove_address(self.address)
