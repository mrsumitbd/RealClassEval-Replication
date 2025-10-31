import http.cookiejar

class Lynx:
    """Class for Lynx"""
    lynx_cookies = ['~/.lynx_cookies', '~/cookies']

    def __init__(self, cookie_file=None, domain_name=''):
        self.cookie_file = _expand_paths(cookie_file or self.lynx_cookies, 'linux')
        self.domain_name = domain_name

    def load(self):
        cj = http.cookiejar.CookieJar()
        if not self.cookie_file:
            raise BrowserCookieError('Cannot find Lynx cookie file')
        with open(self.cookie_file) as f:
            for line in f.read().splitlines():
                domain, domain_specified, path, secure, expires, name, value = [None if word == '' else word for word in line.split('\t')]
                domain_specified = domain_specified == 'TRUE'
                secure = secure == 'TRUE'
                if domain.find(self.domain_name) >= 0:
                    cookie = create_cookie(domain, path, secure, expires, name, value, False)
                    cj.set_cookie(cookie)
        return cj