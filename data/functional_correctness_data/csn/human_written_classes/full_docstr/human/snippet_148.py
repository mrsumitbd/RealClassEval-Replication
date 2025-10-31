import datetime
from txtorcon.util import maybe_ip_addr

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
        self.ip = None
        self.name = None
        self.expiry = None
        self.expires = None
        self.created = None

    def update(self, *args):
        """
        deals with an update from Tor; see parsing logic in torcontroller
        """
        gmtexpires = None
        name, ip, expires = args[:3]
        for arg in args:
            if arg.lower().startswith('expires='):
                gmtexpires = arg[8:]
        if gmtexpires is None:
            if len(args) == 3:
                gmtexpires = expires
            elif args[2] == 'NEVER':
                gmtexpires = args[2]
            else:
                gmtexpires = args[3]
        self.name = name
        self.ip = maybe_ip_addr(ip)
        if self.ip == '<error>':
            self._expire()
            return
        fmt = '%Y-%m-%d %H:%M:%S'
        oldexpires = self.expires
        if gmtexpires.upper() == 'NEVER':
            self.expires = None
        else:
            self.expires = datetime.datetime.strptime(gmtexpires, fmt)
        self.created = datetime.datetime.utcnow()
        if self.expires is not None:
            if oldexpires is None:
                if self.expires <= self.created:
                    diff = datetime.timedelta(seconds=0)
                else:
                    diff = self.expires - self.created
                self.expiry = self.map.scheduler.callLater(diff.seconds, self._expire)
            else:
                diff = self.expires - oldexpires
                self.expiry.delay(diff.seconds)

    def _expire(self):
        """
        callback done via callLater
        """
        del self.map.addr[self.name]
        self.map.notify('addrmap_expired', *[self.name], **{})