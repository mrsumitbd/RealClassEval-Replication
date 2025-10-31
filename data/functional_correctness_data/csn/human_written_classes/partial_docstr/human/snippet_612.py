import re
import time
from typing import Any, cast, Callable, Dict, Optional

class TimeStatistics:

    def __init__(self, expiration: float=300) -> None:
        self.expiration = expiration
        self.data = {}

    def update_callback(self, url: str, callback: Optional[Callable[[], Any]]=None) -> None:
        """Update the statistics for the domain"""
        domain = self.domain(url)
        last_req = self.data.get(domain, 0)
        t_new = time.time()
        do_call = t_new - last_req > self.expiration
        self.data[domain] = t_new
        if do_call and callback:
            callback()

    @staticmethod
    def domain(url: str) -> str:
        match = re.match('^(?:https|mock)://([^/]*)/?', url)
        assert match, "HOST must be including the protocol and :// like 'https://login.salesforce.com'"
        return match.groups()[0]