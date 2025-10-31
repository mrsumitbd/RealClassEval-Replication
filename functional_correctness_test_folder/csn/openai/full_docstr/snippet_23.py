
class StripContentTypeMiddleware:
    '''WSGI middleware to strip Content-Type header for GETs.'''

    def __init__(self, app):
        '''Create the new middleware.
        Args:
            app: a flask application
        '''
        self.app = app

    def __call__(self, environ, start_response):
        '''Run the middleware and then call the original WSGI application.'''
        method = environ.get('REQUEST_METHOD', '').upper()
        if method != 'GET':
            return self.app(environ, start_response)

        def custom_start_response(status, response_headers, exc_info=None):
            filtered_headers = [
                (k, v) for k, v in response_headers
                if k.lower() != 'content-type'
            ]
            return start_response(status, filtered_headers, exc_info)

        return self.app(environ, custom_start_response)
