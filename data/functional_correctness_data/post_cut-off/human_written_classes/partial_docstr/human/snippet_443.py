import json
import urllib3
import ssl
import re
from agntcy_acp.acp_v0.exceptions import ApiException, ApiValueError

class RESTClientObject:

    def __init__(self, configuration) -> None:
        if configuration.verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE
        pool_args = {'cert_reqs': cert_reqs, 'ca_certs': configuration.ssl_ca_cert, 'cert_file': configuration.cert_file, 'key_file': configuration.key_file, 'ca_cert_data': configuration.ca_cert_data}
        if configuration.assert_hostname is not None:
            pool_args['assert_hostname'] = configuration.assert_hostname
        if configuration.retries is not None:
            pool_args['retries'] = configuration.retries
        if configuration.tls_server_name:
            pool_args['server_hostname'] = configuration.tls_server_name
        if configuration.socket_options is not None:
            pool_args['socket_options'] = configuration.socket_options
        if configuration.connection_pool_maxsize is not None:
            pool_args['maxsize'] = configuration.connection_pool_maxsize
        if configuration.timeout is not None:
            if isinstance(configuration.timeout, list) and len(configuration.timeout) == 2:
                pool_args['timeout'] = urllib3.Timeout(connect=configuration.timeout[0], read=configuration.timeout[1])
            elif isinstance(configuration.timeout, (float, int)):
                pool_args['timeout'] = urllib3.Timeout(configuration.timeout)
        self.pool_manager: urllib3.PoolManager
        if configuration.proxy:
            if is_socks_proxy_url(configuration.proxy):
                from urllib3.contrib.socks import SOCKSProxyManager
                pool_args['proxy_url'] = configuration.proxy
                pool_args['headers'] = configuration.proxy_headers
                self.pool_manager = SOCKSProxyManager(**pool_args)
            else:
                pool_args['proxy_url'] = configuration.proxy
                pool_args['proxy_headers'] = configuration.proxy_headers
                self.pool_manager = urllib3.ProxyManager(**pool_args)
        else:
            self.pool_manager = urllib3.PoolManager(**pool_args)

    def request(self, method, url, headers=None, body=None, post_params=None, _request_timeout=None):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        method = method.upper()
        assert method in ['GET', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'OPTIONS']
        if post_params and body:
            raise ApiValueError('body parameter cannot be used with post_params parameter.')
        post_params = post_params or {}
        headers = headers or {}
        timeout = None
        if _request_timeout:
            if isinstance(_request_timeout, (int, float)):
                timeout = urllib3.Timeout(total=_request_timeout)
            elif isinstance(_request_timeout, tuple) and len(_request_timeout) == 2:
                timeout = urllib3.Timeout(connect=_request_timeout[0], read=_request_timeout[1])
        try:
            if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:
                content_type = headers.get('Content-Type')
                if not content_type or re.search('json', content_type, re.IGNORECASE):
                    request_body = None
                    if body is not None:
                        request_body = json.dumps(body)
                    r = self.pool_manager.request(method, url, body=request_body, timeout=timeout, headers=headers, preload_content=False)
                elif content_type == 'application/x-www-form-urlencoded':
                    r = self.pool_manager.request(method, url, fields=post_params, encode_multipart=False, timeout=timeout, headers=headers, preload_content=False)
                elif content_type == 'multipart/form-data':
                    del headers['Content-Type']
                    post_params = [(a, json.dumps(b)) if isinstance(b, dict) else (a, b) for a, b in post_params]
                    r = self.pool_manager.request(method, url, fields=post_params, encode_multipart=True, timeout=timeout, headers=headers, preload_content=False)
                elif isinstance(body, str) or isinstance(body, bytes):
                    r = self.pool_manager.request(method, url, body=body, timeout=timeout, headers=headers, preload_content=False)
                elif headers['Content-Type'].startswith('text/') and isinstance(body, bool):
                    request_body = 'true' if body else 'false'
                    r = self.pool_manager.request(method, url, body=request_body, preload_content=False, timeout=timeout, headers=headers)
                else:
                    msg = 'Cannot prepare a request message for provided\n                             arguments. Please check that your arguments match\n                             declared content type.'
                    raise ApiException(status=0, reason=msg)
            else:
                r = self.pool_manager.request(method, url, fields={}, timeout=timeout, headers=headers, preload_content=False)
        except urllib3.exceptions.SSLError as e:
            msg = '\n'.join([type(e).__name__, str(e)])
            raise ApiException(status=0, reason=msg)
        return RESTResponse(r)