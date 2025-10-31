class StripContentTypeMiddleware:

    def __init__(self, app):
        '''Create the new middleware.
        Args:
            app: a flask application
        '''
        self.app = app

    def __call__(self, environ, start_response):
        # Remove the Content-Type header from the request environment
        environ.pop('CONTENT_TYPE', None)
        return self.app(environ, start_response)
