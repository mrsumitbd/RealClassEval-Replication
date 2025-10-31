import urllib3
import typing as t
from collections import deque
import time
import os

class HttpClient:
    pool_manager: urllib3.PoolManager
    req_count: dict[t.Literal['GET', 'POST'], int]

    def __init__(self) -> None:
        proxy_url = os.environ.get('http_proxy') or os.environ.get('https_proxy')
        headers = {'User-Agent': USER_AGENT}
        if proxy_url:
            self.pool_manager = urllib3.ProxyManager(proxy_url, headers=headers)
        else:
            self.pool_manager = urllib3.PoolManager(headers=headers)
        self.req_count = {'GET': 0, 'POST': 0}
        self._max_t = 3.0
        self._cooloff = 0.16
        self._history = deque([time.time() - self._max_t] * 4, maxlen=4)

    def _limiter(self):
        now = time.time()
        t0 = self._history[0]
        if now - t0 < self._max_t:
            msg = "you're being rate-limited - slow down on the requests! see https://github.com/wimglenn/advent-of-code-data/issues/59 (delay=%.02fs)"
            log.warning(msg, self._cooloff)
            time.sleep(self._cooloff)
            self._cooloff *= 2
            self._cooloff = min(self._cooloff, 10)
        self._history.append(now)

    def get(self, url: str, token: str | None=None, redirect: bool=True) -> urllib3.BaseHTTPResponse:
        if token is None:
            headers = self.pool_manager.headers
        else:
            headers = self.pool_manager.headers | {'Cookie': f'session={token}'}
        self._limiter()
        resp = self.pool_manager.request('GET', url, headers=headers, redirect=redirect)
        self.req_count['GET'] += 1
        return resp

    def post(self, url: str, token: str, fields: t.Mapping[str, str]) -> urllib3.BaseHTTPResponse:
        headers = self.pool_manager.headers | {'Cookie': f'session={token}'}
        self._limiter()
        resp = self.pool_manager.request_encode_body(method='POST', url=url, fields=fields, headers=headers, encode_multipart=False)
        self.req_count['POST'] += 1
        return resp