import http.cookiejar

class W3m:
    """Class for W3m"""
    COO_USE = 1
    COO_SECURE = 2
    COO_DOMAIN = 4
    COO_PATH = 8
    COO_DISCARD = 16
    COO_OVERRIDE = 32
    w3m_cookies = ['~/.w3m/cookie']

    def __init__(self, cookie_file=None, domain_name=''):
        self.cookie_file = _expand_paths(cookie_file or self.w3m_cookies, 'linux')
        self.domain_name = domain_name

    def load(self):
        cj = http.cookiejar.CookieJar()
        if not self.cookie_file:
            raise BrowserCookieError('Cannot find W3m cookie file')
        with open(self.cookie_file) as f:
            for line in f.read().splitlines():
                url, name, value, expires, domain, path, flag, version, comment, port, comment_url = [None if word == '' else word for word in line.split('\t')]
                flag = int(flag)
                expires = int(expires)
                secure = bool(flag & self.COO_SECURE)
                domain_specified = bool(flag & self.COO_DOMAIN)
                path_specified = bool(flag & self.COO_PATH)
                discard = bool(flag & self.COO_DISCARD)
                if domain.find(self.domain_name) >= 0:
                    cookie = http.cookiejar.Cookie(version, name, value, port, bool(port), domain, domain_specified, domain.startswith('.'), path, path_specified, secure, expires, discard, comment, comment_url, {})
                    cj.set_cookie(cookie)
        return cj