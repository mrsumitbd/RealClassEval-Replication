from werkzeug.wsgi import ClosingIterator

class ZappaWSGIMiddleware:
    """
    Middleware functions necessary for a Zappa deployment.

    Most hacks have now been remove except for Set-Cookie permutation.
    """

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        """
        We must case-mangle the Set-Cookie header name or AWS will use only a
        single one of these headers.
        """

        def encode_response(status, headers, exc_info=None):
            """
            This makes the 'set-cookie' headers name lowercase,
            all the non-cookie headers should be sent unharmed.
            Related: https://github.com/Miserlou/Zappa/issues/1965
            """
            new_headers = [header for header in headers if type(header[0]) != str or header[0].lower() != 'set-cookie']
            cookie_headers = [(header[0].lower(), header[1]) for header in headers if type(header[0]) == str and header[0].lower() == 'set-cookie']
            new_headers = new_headers + cookie_headers
            return start_response(status, new_headers, exc_info)
        response = self.application(environ, encode_response)
        return ClosingIterator(response)