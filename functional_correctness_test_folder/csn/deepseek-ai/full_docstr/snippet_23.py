
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
        if environ.get('REQUEST_METHOD') == 'GET' and 'CONTENT_TYPE' in environ:
            del environ['CONTENT_TYPE']
        return self.app(environ, start_response)
