from skydive.tls import create_ssl_context

class Authenticate:

    def __init__(self, endpoint, scheme='http', username='', password='', cookies={}, insecure=False, debug=0, cafile='', certfile='', keyfile=''):
        self.endpoint = endpoint
        self.scheme = scheme
        self.username = username
        self.password = password
        self.cookies = cookies
        self.insecure = insecure
        self.cafile = cafile
        self.certfile = certfile
        self.keyfile = keyfile
        self.debug = debug
        self.cookie_jar = CookieJar()
        self.authenticated = False
        self.token = ''

    def login(self):
        handlers = []
        url = '%s://%s/login' % (self.scheme, self.endpoint)
        handlers.append(request.HTTPHandler(debuglevel=self.debug))
        handlers.append(request.HTTPCookieProcessor(self.cookie_jar))
        data = {'username': self.username, 'password': self.password}
        if self.scheme == 'https':
            context = create_ssl_context(insecure, cafile, certfile, keyfile)
            handlers.append(request.HTTPSHandler(debuglevel=self.debug, context=context))
        opener = request.build_opener(*handlers)
        for k, v in self.cookies.items():
            opener.append = (k, v)
        req = request.Request(url, data=urlencoder.urlencode(data).encode())
        opener.open(req)
        for cookie in self.cookie_jar:
            if cookie.name == 'authtoken':
                self.token = cookie.value
                self.authenticated = True
        return self.authenticated

    def logout(self):
        self.authenticated = False
        self.token = ''