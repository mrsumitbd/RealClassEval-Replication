
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
        def custom_start_response(status, headers, exc_info=None):
            if environ.get('REQUEST_METHOD', '').upper() == 'GET':
                headers = [(k, v)
                           for (k, v) in headers if k.lower() != 'content-type']
            return start_response(status, headers, exc_info)
        return self.app(environ, custom_start_response)
