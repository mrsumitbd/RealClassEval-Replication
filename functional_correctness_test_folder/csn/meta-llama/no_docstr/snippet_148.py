
import time
from collections import OrderedDict


class Addr:

    def __init__(self, map):
        self.map = map
        self.cache = OrderedDict()
        self.ttl = 60  # default TTL in seconds

    def update(self, *args):
        for addr in args:
            self.cache[addr] = time.time()
            if len(self.cache) > self.map:
                self._expire()

    def _expire(self):
        current_time = time.time()
        expired_addrs = [addr for addr, timestamp in self.cache.items(
        ) if current_time - timestamp > self.ttl]
        for addr in expired_addrs:
            del self.cache[addr]
