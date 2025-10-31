from base64 import b64encode
from urllib3.util.retry import Retry
from urllib3 import connection_from_url

class Server:

    def __init__(self, server, **pool_kw):
        socket_options = _get_socket_opts(pool_kw.pop('socket_keepalive', False), pool_kw.pop('socket_tcp_keepidle', None), pool_kw.pop('socket_tcp_keepintvl', None), pool_kw.pop('socket_tcp_keepcnt', None))
        self.pool = connection_from_url(server, socket_options=socket_options, **pool_kw)

    def request(self, method, path, data=None, stream=False, headers=None, username=None, password=None, schema=None, backoff_factor=0, **kwargs):
        """Send a request

        Always set the Content-Length and the Content-Type header.
        """
        if headers is None:
            headers = {}
        if 'Content-Length' not in headers:
            length = super_len(data)
            if length is not None:
                headers['Content-Length'] = length
        if username is not None:
            if 'Authorization' not in headers and username is not None:
                credentials = username + ':'
                if password is not None:
                    credentials += password
                headers['Authorization'] = 'Basic %s' % b64encode(credentials.encode('utf-8')).decode('utf-8')
            if 'X-User' not in headers:
                headers['X-User'] = username
        if schema is not None:
            headers['Default-Schema'] = schema
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        kwargs['assert_same_host'] = False
        kwargs['redirect'] = False
        kwargs['retries'] = Retry(read=0, backoff_factor=backoff_factor)
        return self.pool.urlopen(method, path, body=data, preload_content=not stream, headers=headers, **kwargs)

    def close(self):
        self.pool.close()