
class StripContentTypeMiddleware:

    def __init__(self, app):
        '''Create the new middleware.
        Args:
            app: a flask application
        '''
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, response_headers, exc_info=None):
            response_headers = [
                (header, value) for header, value in response_headers if header != 'Content-Type']
            return start_response(status, response_headers, exc_info)

        return self.app(environ, custom_start_response)
