
class StripContentTypeMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'CONTENT_TYPE' in environ:
            del environ['CONTENT_TYPE']
        return self.app(environ, start_response)
