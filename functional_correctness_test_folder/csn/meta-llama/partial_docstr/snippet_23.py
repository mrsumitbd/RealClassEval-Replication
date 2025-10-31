
class StripContentTypeMiddleware:
    def __init__(self, app):
        '''Create the new middleware.
        Args:
            app: a flask application
        '''
        self.app = app

    def __call__(self, environ, start_response):
        def _start_response(status, headers, *args):
            for i, (header, value) in enumerate(headers):
                if header.lower() == 'content-type':
                    headers.pop(i)
                    break
            return start_response(status, headers, *args)
        return self.app(environ, _start_response)
