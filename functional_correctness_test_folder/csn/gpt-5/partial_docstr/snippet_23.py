class StripContentTypeMiddleware:

    def __init__(self, app):
        '''Create the new middleware.
        Args:
            app: a flask application
        '''
        self.app = app

    def __call__(self, environ, start_response):
        method = environ.get('REQUEST_METHOD', 'GET').upper()
        content_length = environ.get('CONTENT_LENGTH')

        if not content_length or content_length == '0' or method in ('GET', 'HEAD', 'DELETE', 'OPTIONS'):
            environ.pop('CONTENT_TYPE', None)
            environ.pop('HTTP_CONTENT_TYPE', None)

        return self.app(environ, start_response)
